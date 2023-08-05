# Copyright 2019-2020 Stanislav Pidhorskyi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import os
from torch import nn
import torch
from dlutils import async_func
import yacs.config


__all__ = ['Checkpointer']


def get_model_dict(x):
    if x is None:
        return None
    if isinstance(x, nn.DataParallel) or isinstance(x, nn.parallel.DistributedDataParallel):
        return x.module.state_dict()
    else:
        return x.state_dict()


def load_model(x, state_dict, strict):
    if isinstance(x, nn.DataParallel) or isinstance(x, nn.parallel.DistributedDataParallel):
        x.module.load_state_dict(state_dict, strict=strict)
    else:
        x.load_state_dict(state_dict, strict=strict)


class Checkpointer(object):
    def __init__(self, output_dir, models, auxiliary=None, logger=None, save=True):
        self.models = models
        self.auxiliary = auxiliary
        self.output_dir = output_dir.OUTPUT_DIR if isinstance(output_dir, yacs.config.CfgNode) else output_dir
        self.logger = logger
        self._save = save

    def save(self, _name, **kwargs):
        if not self._save:
            return
        data = dict()
        data["models"] = dict()
        data["auxiliary"] = dict()
        for name, model in self.models.items():
            if hasattr(model, 'module') and \
                    (isinstance(model, nn.parallel.DistributedDataParallel) or isinstance(model, nn.parallel.DataParallel)):
                self.logger.info("Stripping away DataParallel wrapping module")
                model = model.module

            data["models"][name] = get_model_dict(model)

        if self.auxiliary is not None:
            for name, item in self.auxiliary.items():
                data["auxiliary"][name] = item.state_dict()
        data.update(kwargs)

        @async_func
        def save_data():
            save_file = os.path.join(self.output_dir, "%s.pth" % _name)
            self.logger.info("Saving checkpoint to %s" % save_file)
            torch.save(data, save_file)
            self.tag_last_checkpoint(save_file)

        return save_data()

    def load(self, ignore_last_checkpoint=False, file_name=None, strict=True):
        save_file = os.path.join(self.output_dir, "last_checkpoint")
        f = None
        try:
            with open(save_file, "r") as last_checkpoint:
                f = last_checkpoint.read().strip()
        except IOError:
            self.logger.warning("No checkpoint found. Initializing model from scratch")
            if file_name is None:
                return {}

        if ignore_last_checkpoint:
            self.logger.info("Forced to Initialize model from scratch")
            return {}
        if file_name is not None:
            f = file_name

        if f is None:
            self.logger.error("Reached unreachable code. Can't load model")
            return

        self.logger.info("Loading checkpoint from {}".format(f))
        checkpoint = torch.load(f, map_location=torch.device("cpu"))
        for name, model in self.models.items():
            if name in checkpoint["models"]:
                try:
                    model_dict = checkpoint["models"].pop(name)
                    if model_dict is not None:
                        load_model(self.models[name], model_dict, strict)
                    else:
                        self.logger.warning("State dict for model \"%s\" is None " % name)
                except RuntimeError as e:
                    self.logger.warning('%s\nFailed to load: %s\n%s' % ('!' * 160, name, '!' * 160))
                    self.logger.warning(e)
            else:
                self.logger.warning("No state dict for model: %s" % name)
        checkpoint.pop('models')
        if "auxiliary" in checkpoint and self.auxiliary:
            self.logger.info("Loading auxiliary from {}".format(f))
            for name, item in self.auxiliary.items():
                try:
                    if name in checkpoint["auxiliary"]:
                        self.auxiliary[name].load_state_dict(checkpoint["auxiliary"].pop(name))
                    if "optimizers" in checkpoint and name in checkpoint["optimizers"]:
                        self.auxiliary[name].load_state_dict(checkpoint["optimizers"].pop(name))
                    if name in checkpoint:
                        self.auxiliary[name].load_state_dict(checkpoint.pop(name))
                except (IndexError, ValueError):
                    self.logger.warning('%s\nFailed to load: %s\n%s' % ('!' * 160, name, '!' * 160))
            checkpoint.pop('auxiliary')

        return checkpoint

    def tag_last_checkpoint(self, last_filename):
        save_file = os.path.join(self.output_dir, "last_checkpoint")
        with open(save_file, "w") as f:
            f.write(last_filename)
