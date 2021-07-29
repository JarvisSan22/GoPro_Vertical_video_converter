import cv2
import numpy as np
import os 
import sys
import glob
import time

#9:16（720 × 1,280px 以上）
newh=1280
neww=720

def frameRotation(frame,angle:float,w:int,h:int):
    a=np.radians(angle)
    scale=1
    center= (w//2,h//2)
    #getRotationMatrix2D関数を使用
    trans = cv2.getRotationMatrix2D(center, angle , scale) 
    #はみだす対策
    rot_w=int(w*abs(np.cos(a)) + h*abs(np.sin(a)))
    rot_h=int(w*abs(np.sin(a)) + h*abs(np.cos(a)))
    #torationのマトリックスを更新する
    trans[0][2] += -w/2 + rot_w/2
    trans[1][2] += -h/2 + rot_h/2
    #アフィン変換
    frame = cv2.warpAffine(frame, trans, (rot_w,rot_h))
    return frame


def captureAndRecordSetup(file,convert_filetype=None):
    cap= cv2.VideoCapture(file)
    filename=file.split(".")[0] # .{}の部分を削除
    filetype=file.split(".")[1]

    view=False

    #総フレーム数を取得
    frame_count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #フレームレート
    frame_rate=int(cap.get(cv2.CAP_PROP_FPS))
    #保存先
    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')#('M','J','P','G') #保存形式
    w=int(cap.get(3)) #幅
    h=int(cap.get(4)) #高さ
    if convert_filetype:
        filetype=convert_filetype

    out = cv2.VideoWriter(f'{filename}_rot.{filetype}',fourcc,frame_rate, (neww,newh))
    return cap,out,filename,filetype,frame_count,frame_rate,w,h

def processVideo(cap,out,w,h,view):
    while True:
        ret,frame=cap.read()
        #print(frame.shape)
        if not ret:
            break


        #angle 90
        angle=-90
        frame=frameRotation(frame,angle,w,h)
        frame=cv2.resize(frame,(neww,newh),interpolation=cv2.INTER_LINEAR)

        #保存
        out.write(frame)
        #表示
        if view:
            cv2.namedWindow("res", cv2.WINDOW_NORMAL)
            cv2.imshow('Frame', cv2.resize(frame,(w//5,h//5)))    #(h//5,w//5)))
            cv2.waitKey(1)

    out.release()
    cap.release()
    cv2.destroyAllWindows()


def main(view):
    print(len(sys.argv))
    if len(sys.argv)<2:
        #Conver all files in folder 
        files=glob.glob("******.MOV")
    else: #Conver all selected files
        files=sys.argv[1:]

    for file in files:
        print(f"{'='*10}")
        print(file)
        
        start = time.time()
        cap,out, _ , _ , _ , _ ,w,h=captureAndRecordSetup(file,"mp4")
        processVideo(cap,out,w,h,view)
        elapses= time.time() - start 
        print(file, " rotated ", elapses)
    

if __name__=="__main__":
    view=True
    main(view)
