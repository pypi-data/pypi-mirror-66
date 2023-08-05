import argparse
from numbers import Number

import numpy as np
import torch
from tqdm import tqdm

from .summarize import SummarizerCollection
from .utils import print_num_params


class BaseExperimentManager:
    """
    Experiment manager.

    Data attributes:
    - 'args': argparse.Namespace containing all config parameters. When
      initializing this object, if 'args' is not given, all config
      parameters are set based on experiment defaults and user input, using
      argparse.
    - 'run_description': string description of the run that includes a timestamp
      and can be used e.g. as folder name for logging.
    - 'model': the model.
    - 'device': torch.device that is being used
    - 'dataloaders': DataLoaders, with attributes 'train' and 'test'
    - 'optimizer': the optimizer
    """

    def __init__(self, args=None):
        self.device = None
        self.dataloaders = None
        self.model = None
        self.optimizer = None
        self.args = args
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            allow_abbrev=False)
        if args is None:
            self.args = self._parse_args(parser)
        self.run_description = self._make_run_description(self.args)


    def _parse_args(self, parser):
        """
        Parse command-line arguments defining experiment settings.

        :return: args: argparse.Namespace with experiment settings
        """
        raise NotImplementedError


    def add_required_args(self,
                          parser,
                          batch_size=None,
                          test_batch_size=None,
                          lr=None,
                          max_epochs=1000000,
                          max_steps=2147483647,
                          seed=54321,
                          train_log_every=10000,
                          test_log_every=10000,
                          checkpoint_every=100000,
                          keep_checkpoint_max=3,
                          resume="",
                          ):

        parser.add_argument('--batch-size',
                            type=int,
                            default=batch_size,
                            metavar='N',
                            dest='batch_size',
                            help='training batch size')

        parser.add_argument('--test-batch-size',
                            type=int,
                            default=test_batch_size,
                            metavar='N',
                            dest='test_batch_size',
                            help='test batch size')

        parser.add_argument('--lr',
                            type=float,
                            default=lr,
                            metavar='LR',
                            dest='lr',
                            help='learning rate')

        parser.add_argument('--seed',
                            type=int,
                            default=seed,
                            metavar='N',
                            dest='seed',
                            help='random seed')

        parser.add_argument('--tr-log-every',
                            type=int,
                            default=train_log_every,
                            metavar='N',
                            dest='train_log_every',
                            help='log training metrics every this number of '
                                 'training steps')

        parser.add_argument('--ts-log-every',
                            type=int,
                            default=test_log_every,
                            metavar='N',
                            dest='test_log_every',
                            help='log test metrics every this number of '
                                 'training steps')

        parser.add_argument('--checkpoint-every',
                            type=int,
                            default=checkpoint_every,
                            metavar='N',
                            dest='checkpoint_every',
                            help='save model checkpoint every this number of '
                                 'training steps')

        parser.add_argument('--keep-checkpoint-max',
                            type=int,
                            default=keep_checkpoint_max,
                            metavar='N',
                            dest='keep_checkpoint_max',
                            help='keep at most this number of most recent '
                                 'model checkpoints')

        parser.add_argument('--max-steps',
                            type=int,
                            default=max_steps,
                            metavar='N',
                            dest='max_steps',
                            help='max number of training steps')

        parser.add_argument('--max-epochs',
                            type=int,
                            default=max_epochs,
                            metavar='N',
                            dest='max_epochs',
                            help='max number of training epochs')

        parser.add_argument('--nocuda',
                            action='store_true',
                            dest='no_cuda',
                            help='do not use cuda')

        parser.add_argument('--descr',
                            type=str,
                            default='',
                            metavar='STR',
                            dest='additional_descr',
                            help='additional description for experiment name')

        parser.add_argument('--dry-run',
                            action='store_true',
                            dest='dry_run',
                            help='do not save anything to disk')

        parser.add_argument('--resume',
                            type=str,
                            metavar='NAME',
                            default=resume,
                            dest='resume',
                            help="load the run with this name and resume training")


    @staticmethod
    def _make_run_description(args):
        """
        Create a string description of the run. It is used in the names of the
        logging folders.

        :param args: experiment config
        :return: the run description
        """
        raise NotImplementedError


    def make_datamanager(self):
        """
        Create a DatasetManager object. To be overridden.
        :return: DatasetManager
        """
        raise NotImplementedError


    def make_model(self):
        """
        Create a model. To be overridden.
        :return: model
        """
        raise NotImplementedError


    def make_optimizer(self):
        """
        Create an optimizer. To be overridden.
        :return: optimizer
        """
        raise NotImplementedError


    def setup(self, checkpoint_folder=None):
        """
        Setup experiment: load dataset, create model, load weights if a
        checkpoint is given, create optimizer.
        """

        # If checkpoint folder is given, load model from there to resume
        resume = checkpoint_folder is not None

        # Dataset
        print("Getting dataset ready...")
        self.dataloaders = self.make_datamanager()
        print("Data shape: {}".format(self.dataloaders.data_shape))
        print("Train/test set size: {}/{}".format(
            len(self.dataloaders.train.dataset),
            len(self.dataloaders.test.dataset),
        ))

        # Model
        print("Creating model...")
        self.model = self.make_model().to(self.device)
        print_num_params(self.model)

        # Load weights if resuming training
        if resume:
            self.load_model(checkpoint_folder, step=None)

        # Optimizer
        self.optimizer = self.make_optimizer()


    def load_model(self, checkpoint_folder, step=None):
        """
        Loads model weights from a checkpoint in the specified folder.
        If step is given, it attempts to load the checkpoint at that step.
        The weights are loaded with map_location=device, where device is the
        current device of this experiment.
        """
        self.model.load(checkpoint_folder, self.device, step=step)


    def forward_pass(self, x, y=None):
        """
        Simple single-pass model evaluation. It consists of a forward pass
        and computation of all necessary losses and metrics.
        """
        raise NotImplementedError


    def post_backward_callback(self):
        pass


    @classmethod
    def get_metrics_dict(cls, results):
        """
        Given a dict of results, return a dict of metrics to be given to
        summarizers. Keys are also used as names for tensorboard logging.

        In the base implementation, keys are simply copyed and used as names
        for tensorboard.

        Only scalars accepted, non-scalars are discarded. Actually, anything
        that either is a scalar or has the method item(). That should include
        Python scalars, numpy scalars, torch scalars, numpy and torch
        arrays/tensors with one element.

        Override to customize translation from results to dictionary of
        scalar metrics.
        """
        metrics_dict = {}
        for k in results:
            x = results[k]
            if isinstance(x, Number):
                metrics_dict[k] = x
                continue
            try:
                metrics_dict[k] = x.item()
            except (AttributeError, ValueError):  # is this enough?
                pass
        return metrics_dict


    @classmethod
    def train_log_str(cls, summaries, step, epoch=None):
        s = "       [step {}]".format(step)
        for k in summaries:
            s += "  {key}={value:.5g}".format(key=k, value=summaries[k])
        return s


    @classmethod
    def test_log_str(cls, summaries, step, epoch=None):
        s = "       "
        if epoch is not None:
            s += "[step {}, epoch {}]".format(step, epoch)
        for k in summaries:
            s += "  {key}={value:.5g}".format(key=k, value=summaries[k])
        return s


    def test_procedure(self, **kwargs):
        """
        Execute test procedure for the experiment. This typically includes
        collecting metrics on the test set using forward_pass().
        For example in variational inference we might be interested in
        repeating this many times to derive the importance-weighted ELBO.

        :return: summaries (dict)
        """
        raise NotImplementedError


    def additional_testing(self, img_folder):
        """
        Perform additional testing, including possibly generating images.

        :param img_folder: folder to store images
        """
        raise NotImplementedError


class VIExperimentManager(BaseExperimentManager):
    """
    Variational inference experiment manager. This version implements a default
    test_procedure for variational inference.

    Data attributes:
    - 'args': argparse.Namespace containing all config parameters. When
      initializing this object, if 'args' is not given, all config
      parameters are set based on experiment defaults and user input, using
      argparse.
    - 'run_description': string description of the run that includes a timestamp
      and can be used e.g. as folder name for logging.
    - 'model': the model.
    - 'device': torch.device that is being used
    - 'dataloaders': DataLoaders, with attributes 'train' and 'test'
    - 'optimizer': the optimizer
    """

    def test_procedure(self, iw_samples=None):
        """
        Execute test procedure for the experiment. This typically includes
        collecting metrics on the test set using forward_pass().
        Repeat this many times to derive the importance-weighted ELBO.

        :param iw_samples: number of samples for the importance-weighted ELBO.
                The other metrics are also averaged over all these samples,
                yielding a more accurate estimate.
        :return: summaries (dict)
        """

        # Shorthand
        test_loader = self.dataloaders.test
        step = self.model.global_step
        args = self.args
        n_test = len(test_loader.dataset)

        # If it's time to estimate log likelihood, use many samples.
        # If given, use the given number.
        if iw_samples is None:
            iw_samples = 1
            if step % args.loglikelihood_every == 0 and step > 0:
                iw_samples = args.loglikelihood_samples

        # Setup
        summarizers = SummarizerCollection(mode='sum')
        progress = tqdm(total=len(test_loader) * iw_samples, desc='test ')
        all_elbo_sep = torch.zeros(n_test, iw_samples)
        for batch_idx, (x, y) in enumerate(test_loader):
            for i in range(iw_samples):
                outputs = self.forward_pass(x, y)

                # elbo_sep shape (batch size,)
                i_start = batch_idx * args.test_batch_size
                i_end = (batch_idx + 1) * args.test_batch_size
                all_elbo_sep[i_start: i_end, i] = outputs['elbo_sep'].detach()

                metrics_dict = self.get_metrics_dict(outputs)
                multiplier = (x.size(0) / n_test) / iw_samples
                for k in metrics_dict:
                    metrics_dict[k] *= multiplier
                summarizers.add(metrics_dict)

                progress.update()
        progress.close()

        if iw_samples > 1:
            # Shape (test set size,)
            elbo_iw = torch.logsumexp(all_elbo_sep, dim=1)
            elbo_iw = elbo_iw - np.log(iw_samples)

            # Mean over test set (scalar)
            elbo_iw = elbo_iw.mean().item()
            key = 'elbo/elbo_IW_{}'.format(iw_samples)
            summarizers.add({key: elbo_iw})

        summaries = summarizers.get_all(reset=True)

        return summaries


    def add_required_args(self,
                          parser,
                          loglikelihood_every=50000,
                          loglikelihood_samples=100,
                          **kwargs
                          ):

        super().add_required_args(parser, **kwargs)

        parser.add_argument('--ll-every',
                            type=int,
                            default=loglikelihood_every,
                            metavar='N',
                            dest='loglikelihood_every',
                            help='evaluate log likelihood every this number '
                                 'of training steps')

        parser.add_argument('--ll-samples',
                            type=int,
                            default=loglikelihood_samples,
                            metavar='N',
                            dest='loglikelihood_samples',
                            help='number of importance-weighted samples to '
                                 'evaluate log likelihood')
