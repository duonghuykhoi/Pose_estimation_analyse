import tensorflow as tf
import cv2
import time
import argparse
import os
import csv
import pandas as pd
import posenet
import json
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--scale_factor', type=float, default=1.0)
parser.add_argument('--notxt', action='store_true')
parser.add_argument('--image_dir', type=str, default='./images')
parser.add_argument('--output_dir', type=str, default='./output')
parser.add_argument('--outputcsv_dir', type=str, default='./outputcsv')
parser.add_argument('--outputjson_dir', type=str, default='./outputjson')
parser.add_argument('--name', type=str, default='Squat_Video')
args = parser.parse_args()


def main():
  
    with tf.Session() as sess:
        model_cfg, model_outputs = posenet.load_model(args.model, sess)
        output_stride = model_cfg['output_stride']

        if args.output_dir:
            if not os.path.exists(args.output_dir):
                os.makedirs(args.output_dir)
                
        if args.outputcsv_dir:
            if not os.path.exists(args.outputcsv_dir):
                os.makedirs(args.outputcsv_dir)

        if args.outputjson_dir:
            if not os.path.exists(args.outputjson_dir):
                os.makedirs(args.outputjson_dir)

        filenames = [
            f.path for f in os.scandir(args.image_dir) if f.is_file() and f.path.endswith(('.png', '.jpg'))]
        filenames.sort()
        start = time.time()
        count=0
        lic1=[]
        lic3=[]
        for f in filenames:
            input_image, draw_image, output_scale = posenet.read_imgfile(
                f, scale_factor=args.scale_factor, output_stride=output_stride)

            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
                model_outputs,
                feed_dict={'image:0': input_image}
            )

            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multiple_poses(
                heatmaps_result.squeeze(axis=0),
                offsets_result.squeeze(axis=0),
                displacement_fwd_result.squeeze(axis=0),
                displacement_bwd_result.squeeze(axis=0),
                output_stride=output_stride,
                max_pose_detections=10,
                min_pose_score=0.1)

            keypoint_coords *= output_scale

            d=list()

            # print(np.amax(pose_scores))
            # print(np.where(pose_scores == np.amax(pose_scores)))
            # print(pose_scores[np.where(pose_scores == np.amax(pose_scores))])
            # for pi in range(len(pose_scores)):
            #         if pose_scores[pi] == 0.:
            #             break
            #         for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
            #           d.append([posenet.PART_NAMES[ki], s, c, pose_scores[pi]])
            pi= int(np.where(pose_scores == np.amax(pose_scores))[0])
            print(pi)
            for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
                d.append([posenet.PART_NAMES[ki], s, c, pose_scores[pi]])


            if args.output_dir:
                draw_image = posenet.draw_skel_and_kp(
                    draw_image, pose_scores, keypoint_scores, keypoint_coords,
                    min_pose_score=0.1, min_part_score=0.05)

                cv2.imwrite(os.path.join(args.output_dir, os.path.relpath(f, args.image_dir)), draw_image)

            if args.outputcsv_dir:
              count=count+1
              column_names = ['Part_name','Score','Coord', 'Pose_scores']
              df = pd.DataFrame(d, columns=column_names)
              df.to_csv (os.path.join(args.outputcsv_dir, os.path.relpath(f, args.image_dir))+'.csv', index = False, header=True)
              

            lic2=[]
            for i in range(len(d)):
              lic2.append({'score':d[i][1],'part':d[i][0],'position':dict({'x':d[i][2][0],'y':d[i][2][1]})})
            
            lic1.append([{'score':pose_scores[0],'keypoints':lic2}])
            
           
            if not args.notxt:
                print()
                print("Results for image: %s" % f)
                for pi in range(len(pose_scores)):
                    if pose_scores[pi] == 0.:
                        break
                    print('Pose #%d, score = %f' % (pi, pose_scores[pi]))
                    for ki, (s, c) in enumerate(zip(keypoint_scores[pi, :], keypoint_coords[pi, :, :])):
                        print('Keypoint %s, score = %f, coord = %s' % (posenet.PART_NAMES[ki], s, c))

                       
        final_dict = dict({'data':lic1})
        
        if args.outputjson_dir:
          with open(args.outputjson_dir +"/"+ args.name + '.json', 'w') as fz:
            fz.close()
          with open(args.outputjson_dir +"/"+ args.name + '.json', 'r+') as fp:
            json.dump(final_dict, fp)
        
        

if __name__ == "__main__":
    main()
