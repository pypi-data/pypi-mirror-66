"""
    Copyright (C) 2020 Shandong University

    This program is licensed under the GNU General Public License 3.0 
    (https://www.gnu.org/licenses/gpl-3.0.html). 
    Any derivative work obtained under this license must be licensed 
    under the GNU General Public License as published by the Free 
    Software Foundation, either Version 3 of the License, or (at your option) 
    any later version, if this derivative work is distributed to a third party.

    The copyright for the program is owned by Shandong University. 
    For commercial projects that require the ability to distribute 
    the code of this program as part of a program that cannot be 
    distributed under the GNU General Public License, please contact 
            
            sailist@outlook.com
             
    to purchase a commercial license.
"""

import os
import warnings
from functools import wraps

from .meter import AvgMeter
from .meter import Meter
from .params import Params
from .trainer import BaseTrainer
from ..base_classes.trickitems import NoneItem, AvgItem


class BaseCallback():
    """
    基类

    除了基本的回调接口外，还实现了`auto_hook`和`reverse_hook`两个方法，
    用来将callback实现的方法绑定到trainer和将trainer所有可回调的函数绑定到callback中。

    因为绑定的方法只会调用on_begin()和on_end()，因此对于具体的方法需要进行判断进行方法的分流，或者不使用自动绑定，
    而是主动用trainer绑定::

        trainer.add_callback(func=trainer.train, callback=cb)

    """
    priority = 0  # 所有内部实现的Callback优先级均在 [0-100] 以内

    def __new__(cls, *_, **__):
        self = super().__new__(cls)
        self.enable = True

        def ecp_wrap(func):
            """同一个异常第一次调用的时候运行"""

            @wraps(func)
            def on_exception(trainer: BaseTrainer, tfunc, param: Params, e: BaseException, *args, **kwargs):
                self.ecp = getattr(self, "ecp", None)
                res = None
                if self.ecp != e:
                    res = self.on_first_exception(trainer, tfunc, param, e, *args, **kwargs)
                    self.ecp = e

                eres = func(trainer, tfunc, param, e, *args, **kwargs)
                if res is None:
                    return eres
                else:
                    return res


            return on_exception

        self.on_exception = ecp_wrap(self.on_exception)
        return self

    def on_hooked(self, trainer: BaseTrainer, param: Params):
        """called when callback hooked trainer"""
        trainer.logger.info("{} hooked on {}.".format(self, trainer))

    def on_first_exception(self, trainer: BaseTrainer, func, param: Params, e: BaseException, *args, **kwargs):
        """
        when an exception was raised in some function, on_exception() will be called.

        如果异常发生在一个嵌套调用的函数中，那么该异常会在每一层函数都raise一次。

        该方法将被调用当该异常第一次raise出来的时候。
        该方法在 __new__ 中作了处理逻辑，不受继承关系影响
        """
        pass

    def on_exception(self, trainer: BaseTrainer, func, param: Params, e: BaseException, *args, **kwargs):
        """called when exception raised in some function"""
        return False

    def on_hook_failed(self, trainer, message):
        """Any reason when callback cannot hook on trainer"""
        pass

    def on_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        """called before trainer.func is called"""
        pass

    def on_end(self, trainer: BaseTrainer, func, param: Params, meter, *args, **kwargs):
        pass

    def __le__(self, other):
        return self.priority <= other.priority

    def __lt__(self, other):
        return self.priority < other.priority

    def hook(self, trainer: BaseTrainer):
        """自动将自己已有的on_func_begin/on_func_end方法绑定"""
        trainer.add_callback(self)
        self._trainer = trainer

    def unhook(self):
        self._trainer.remove_callback(self)

    def _repr_by_val(self, *vals):
        vstr = "; ".join(["{}={}".format(val, str(getattr(self, val, None))) for val in vals])
        return "{}([{}])".format(self.__class__.__name__, vstr)

    def __repr__(self) -> str:
        return self._repr_by_val("priority")


class TrainCallback(BaseCallback):
    """
    实现了一般训练过程中的函数函数回调
    """

    def on_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        if func.__name__ == "train":
            self.on_train_begin(trainer, func, param, *args, **kwargs)
        elif func.__name__ == "train_epoch":
            self.on_train_epoch_begin(trainer, func, param, *args, **kwargs)
        elif func.__name__ == "train_batch":
            self.on_train_batch_begin(trainer, func, param, *args, **kwargs)
        elif func.__name__ == "test":
            self.on_test_begin(trainer, func, param, *args, **kwargs)
        elif func.__name__ == "eval":
            self.on_eval_begin(trainer, func, param, *args, **kwargs)

    def on_train_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        pass

    def on_train_epoch_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        pass

    def on_test_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        pass

    def on_eval_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        pass

    def on_train_batch_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        pass

    def on_end(self, trainer: BaseTrainer, func, param: Params, meter, *args, **kwargs):
        if func.__name__ == "train":
            self.on_train_end(trainer, func, param, meter, *args, **kwargs)
        elif func.__name__ == "train_epoch":
            self.on_train_epoch_end(trainer, func, param, meter, *args, **kwargs)
        elif func.__name__ == "train_batch":
            self.on_train_batch_end(trainer, func, param, meter, *args, **kwargs)
        elif func.__name__ == "test":
            self.on_test_end(trainer, func, param, meter, *args, **kwargs)
        elif func.__name__ == "eval":
            self.on_eval_end(trainer, func, param, meter, *args, **kwargs)

    def on_train_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        pass

    def on_train_epoch_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        pass

    def on_test_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        pass

    def on_eval_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        pass

    def on_train_batch_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        pass


class EvalCallback(TrainCallback):
    """决定在训练过程中，几个epoch eval一次，几个epoch  test一次"""

    def __init__(self, eval_per_epoch=1, test_per_epoch=10):
        self.eval_in_per_epoch = eval_per_epoch
        self.test_in_per_epoch = test_per_epoch

    def on_train_epoch_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        if param.eidx % self.eval_in_per_epoch == self.eval_in_per_epoch - 1:
            trainer.eval()
        if param.eidx % self.test_in_per_epoch == self.test_in_per_epoch - 1:
            trainer.test()

    def on_train_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        if param.eidx % self.eval_in_per_epoch != self.eval_in_per_epoch - 1:
            trainer.eval()
        if param.eidx % self.test_in_per_epoch != self.test_in_per_epoch - 1:
            trainer.test()

    def __repr__(self):
        return self._repr_by_val("eval_in_per_epoch", "test_per_epoch")


class LoggerCallback(TrainCallback):
    def __init__(self, avg=True):
        self.avg = avg

    def on_hooked(self, trainer: BaseTrainer, param: Params):
        super().on_hooked(trainer, param)
        trainer.logger.info("Exp BaseDir", os.path.abspath(trainer.experiment.exp_dir))
        trainer.logger.info("Exp Trainer", trainer.__class__.__name__)
        trainer.logger.info("Exp Params", param)

    def on_train_epoch_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        if self.avg:
            self.meter = AvgMeter()
        trainer.logger.info("{}/{}".format(param.eidx, param.epoch), prefix="train epoch")

    def on_train_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        super().on_train_begin(trainer, func, param, *args, **kwargs)

    def on_train_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        if meter is None:
            meter = ""
        trainer.logger.info("train end", meter)

    def on_train_batch_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        if meter is None:
            meter = ""
        else:

            if self.avg:
                self.meter.update(meter)
                meter = self.meter
        trainer.logger.inline("{}/{}".format(param.idx, len(trainer.iter_train_dataloader())), meter, fix=1)

    def on_first_exception(self, trainer: BaseTrainer, func, param: Params, e: BaseException, *args, **kwargs):
        trainer.logger.error("{} raised".format(e.__class__.__name__))

    def on_test_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        trainer.logger.info("tests start")

    def on_eval_begin(self, trainer: BaseTrainer, func, param: Params, *args, **kwargs):
        trainer.logger.info("eval start")

    def on_eval_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        if meter is None:
            meter = ""
        trainer.logger.info("eval end", meter)

    def on_test_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        if meter is None:
            meter = ""
        trainer.logger.info("tests end", meter)


class ModelCheckpoint(TrainCallback):
    def __init__(self, monitor, mode="train", lower=True, start_epoch=0):
        self.monitor = monitor
        self.mode = mode
        self.lower = lower
        self.last_val = NoneItem()
        self.start_epoch = start_epoch

    def on_train_epoch_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        self.update("train", trainer, param, meter)

    def update(self, cur_mode, trainer, param, meter):
        if cur_mode != self.mode:
            return
        if param.eidx > self.start_epoch:
            item = meter[self.monitor]
            if isinstance(item, AvgItem):
                item = item.avg
            if isinstance(item, NoneItem):
                return

            if self.lower:
                if self.last_val > item:
                    trainer.logger.info("model imporved from {} to {}".format(self.last_val, item))
                    trainer.save_checkpoint(meter.serialize())
                    self.last_val = item
            else:
                if self.last_val < item:
                    trainer.logger.info("model imporved from {} to {}".format(self.last_val, item))
                    trainer.save_checkpoint(meter.serialize())
                    self.last_val = item

    def on_test_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        self.update("test", trainer, param, meter)

    def on_eval_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        self.update("eval", trainer, param, meter)


class TimingCheckpoint(TrainCallback):
    def __init__(self, per_epoch):
        self.per_epoch = per_epoch

    def on_train_epoch_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        if param.eidx % self.per_epoch == 0 and param.eidx > 0:
            trainer.save_keypoint(meter.serialize(), replacement=True)


class BoardCallback(TrainCallback):
    def __init__(self, unit="epoch", empty_mode="zero"):
        """
        :param unit: epoch or global_step
        :param empty_mode: 'zero': default = 0 or 'ignore' :not record
        """
        self.watch_dict = dict(
            train=dict(),
            test=dict(),
            eval=dict(),
        )
        self.unit = unit
        self.empty_mode = empty_mode

    def watch_scalars(self, mode, names_pair, tag):
        """
        like
            watch_scalars("train", {"all_loss":"all","a_loss":"a"}, "losses") or
            watch_scalars("train", [("all_loss","all"), ("a_loss","a")], "losses")

        如果只有一对，那么调用 add_scalar
        如果只有多对，那么调用 add_scalars
        :param mode:
        :param names_pair:
        :param tag:
        :return:
        """
        assert tag not in self.watch_dict[mode], "{} exists in {} watch dict".format(tag, mode)
        self.watch_dict[mode][tag] = names_pair

    def watch_scalar(self, mode, name, tag):
        assert tag not in self.watch_dict[mode], "{} exists in {} watch dict".format(tag, mode)
        self.watch_dict[mode][tag] = name

    def _find_value(self, meter: Meter, key):
        if isinstance(meter[key], AvgItem):
            return meter[key].avg
        elif isinstance(meter[key], NoneItem):
            if self.empty_mode == "zero":
                return 0
            else:
                return None
        elif isinstance(meter[key], (str)):
            warnings.warn("tensorboard scalar types can't be str, but meter.{} is".format(key))
            return None
        return meter[key]

    def on_train_epoch_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        self.update(trainer,meter,param,"train")

    def update(self,trainer,meter,param,mode):
        from thexp.utils.generel_util import iter2pair
        step = param.eidx if self.unit == "epoch" else param.global_step

        for tag, names in self.watch_dict[mode].items():
            if isinstance(names, str):
                val = self._find_value(meter, names)
                if val is not None:
                    trainer.writter.add_scalar(tag, val, step)
            else:
                scalar_dict = {}
                for k, v in iter2pair(names):
                    val = self._find_value(meter, k)
                    if val is not None:
                        scalar_dict[v] = val
                trainer.writter.add_scalars(tag, scalar_dict, step)

    def on_eval_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        self.update(trainer,meter,param,"eval")

    def on_test_end(self, trainer: BaseTrainer, func, param: Params, meter: Meter, *args, **kwargs):
        self.update(trainer,meter,param,"test")


class KeyErrorSave(TrainCallback):
    priority = -1
    def __init__(self,wait_input=False):
        self.wait_input=wait_input

    def on_first_exception(self, trainer: BaseTrainer, func, param: Params, e: BaseException, *args, **kwargs):
        if isinstance(e,(KeyboardInterrupt)):
            trainer.logger.info("KeyErrorSave trigged, save checkpoint")
            trainer.save_keypoint({"mode":"KeyboardInterrupt"})

            tp = "n"
            if self.wait_input:
                tp = input("continue train step? (y/other)")

            if tp.lower() == "y":
                return True



class CUDAErrorHold(TrainCallback):
    priority = -1
    def __init__(self,wait_input=False):
        self.wait_input=wait_input
    def on_first_exception(self, trainer: BaseTrainer, func, param: Params, e: BaseException, *args, **kwargs):
        if isinstance(e,(RuntimeError)):
            if "cuda" in str(e).lower():
                trainer.logger.info("CUDA Error trigged, enter to continue or type any to exit")
                tp = input("enter to continue or any other type to exit?")

                if len(tp.strip()) == 0:
                    return True