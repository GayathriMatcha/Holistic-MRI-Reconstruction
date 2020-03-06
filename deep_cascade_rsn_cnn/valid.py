import pathlib
import sys
from collections import defaultdict
import argparse
import numpy as np
import torch
from torch.utils.data import DataLoader
from dataset import SliceDataDev,KneeDataDev
from models import DnCn
import h5py
from tqdm import tqdm

def save_reconstructions(reconstructions, out_dir):
    """
    Saves the reconstructions from a model into h5 files that is appropriate for submission
    to the leaderboard.
    Args:
        reconstructions (dict[str, np.array]): A dictionary mapping input filenames to
            corresponding reconstructions (of shape num_slices x height x width).
        out_dir (pathlib.Path): Path to the output directory where the reconstructions
            should be saved.
    """
    out_dir.mkdir(exist_ok=True)
    for fname, recons in reconstructions.items():
        with h5py.File(out_dir / fname, 'w') as f:
            f.create_dataset('reconstruction', data=recons)

def create_data_loaders(args):

    if args.dataset_type == 'knee':
        data = KneeDataDev(args.data_path,args.acceleration_factor,args.dataset_type)
        data_loader = DataLoader(
            dataset=data,
            batch_size=args.batch_size,
            num_workers=1,
            pin_memory=True,)
    else:
        data = SliceDataDev(args.data_path,args.acceleration_factor,args.dataset_type)
        data_loader = DataLoader(
            dataset=data,
            batch_size=args.batch_size,
            num_workers=1,
            pin_memory=True,)

    return data_loader



def load_model(checkpoint_file):
    checkpoint = torch.load(checkpoint_file)
    args = checkpoint['args']
    model = DnCn(args,n_channels=1).to(args.device)
    #print(model)
    if args.data_parallel:
        model = torch.nn.DataParallel(model)
    model.load_state_dict(checkpoint['model'])
    return model


def run_unet(args, model, data_loader):
    model.eval()
    reconstructions = defaultdict(list)
    with torch.no_grad():
        for (iter,data) in enumerate(tqdm(data_loader)):


            if args.dataset_type == 'knee' :
                input, input_kspace, target,fnames = data
            else:
                input, input_kspace, target,fnames,slices = data

            input = input.unsqueeze(1).to(args.device)
            #input_kspace = input_kspace.unsqueeze(1).to(args.device)
            input_kspace = input_kspace.permute(0,3,1,2).to(args.device)
            input = input.float()
            input_kspace = input_kspace.float()
            recons = model(input,input_kspace).to('cpu').squeeze(1)

#            if args.dataset_type == 'cardiac':
                #recons = recons[:,5:155,5:155]

            if args.dataset_type == 'knee':
                for i in range(recons.shape[0]):
                    recons[i] = recons[i] 
                    reconstructions[fnames[i]].append(recons[i].numpy())

            else :
                for i in range(recons.shape[0]):
                    recons[i] = recons[i] 
                    reconstructions[fnames[i]].append((slices[i].numpy(), recons[i].numpy()))

    if args.dataset_type == 'knee':

        reconstructions = {
            fname: np.stack([pred for pred in sorted(slice_preds)])
            for fname, slice_preds in reconstructions.items()
        }

    else:
         reconstructions = {
             fname: np.stack([pred for _, pred in sorted(slice_preds)])
             for fname, slice_preds in reconstructions.items()
         }


            
    return reconstructions


def main(args):
    
    data_loader = create_data_loaders(args)
    model = load_model(args.checkpoint)
    reconstructions = run_unet(args, model, data_loader)
    save_reconstructions(reconstructions, args.out_dir)


def create_arg_parser():

    parser = argparse.ArgumentParser(description="Valid setup for MR recon U-Net")
    parser.add_argument('--checkpoint', type=pathlib.Path, required=True,
                        help='Path to the U-Net model')
    parser.add_argument('--out-dir', type=pathlib.Path, required=True,
                        help='Path to save the reconstructions to')
    parser.add_argument('--batch-size', default=16, type=int, help='Mini-batch size')
    parser.add_argument('--device', type=str, default='cuda', help='Which device to run on')
    parser.add_argument('--data-path',type=str,help='path to validation dataset')

    parser.add_argument('--acceleration_factor',type=str,help='acceleration factors')
    parser.add_argument('--dataset_type',type=str,help='cardiac,kirby')
    parser.add_argument('--usmask_path',type=str,help='undersampling mask path')
    #parser.add_argument('--unet_model_path',type=str,help='unet best model path')
    #parser.add_argument('--dautomap_model_path',type=str,help='dautomap best model path')
    
    return parser

if __name__ == '__main__':
    args = create_arg_parser().parse_args(sys.argv[1:])
    main(args)
