import cv2
from numpy import *
import os
import matplotlib.pyplot as plt

screenLevels = 255.0


def yuv_import(filename, dims, numfrm, startfrm):
    fp = open(filename, 'rb')
    blk_size = prod(dims) * 3 / 2
    fp.seek(int(blk_size) * int(startfrm), 0)
    Y = []
    U = []
    V = []
    d00 = dims[0] // 2
    d01 = dims[1] // 2
    Yt = zeros((dims[0], dims[1]), uint8, 'C')
    Ut = zeros((d00, d01), uint8, 'C')
    Vt = zeros((d00, d01), uint8, 'C')
    for i in range(numfrm):
        for m in range(dims[0]):
            for n in range(dims[1]):
                # print m,n
                Yt[m, n] = ord(fp.read(1))
        for m in range(d00):
            for n in range(d01):
                Ut[m, n] = ord(fp.read(1))
        for m in range(d00):
            for n in range(d01):
                Vt[m, n] = ord(fp.read(1))
        Y = Y + [Yt]
        U = U + [Ut]
        V = V + [Vt]
    fp.close()
    return (Y, U, V)


def MSE(mode, n, width, height):  # 第二个坐标是width
    MseCount = 0
    MsePerFrameList = list()
    for i in range(150):
        DiffCount = 0
        DataOri = yuv_import('football_cif.yuv', (height, width), 1, i)
        if mode == 1:
            DataNew = yuv_import(
                r'F:/Master/NTU/6427-Video Signal Process/Assignment/h263/Decoder data/q%ddecode.yuv' % n,
                (height, width), 1, i)
        elif mode == 2:
            DataNew = yuv_import(
                r'F:/Master/NTU/6427-Video Signal Process/Assignment/h263/Decoder data/q2_r%d000.yuv' % n,
                (height, width), 1, i)
        for j in range(height):
            for k in range(width):
                DiffPerPixel = (int(DataNew[0][0][j][k]) - int(DataOri[0][0][j][k])) ** 2
                DiffCount += DiffPerPixel
        MsePerFrame = DiffCount / (width * height)
        MsePerFrameList.append(MsePerFrame)
        MseCount += MsePerFrame
    Mse = MseCount / 150
    return Mse, MsePerFrameList


def drawPSNR():
    Bitrate = [5355, 3785, 2719, 2211, 1763, 1523, 1284, 1148, 1000, 913, 817, 758, 690, 648,
               599, 568, 530, 507, 478, 460, 437, 422, 405, 392]
    for n in range(2, 26):
        Mse, MsePerFrameList = MSE(1, n, width, height)
        MseList.append(Mse)
        PSNR = 10 * log10(255 ** 2 / Mse)
        PSNRList.append(PSNR)
        print("Q%d's Mse is:" % n, Mse)
        print("Q%d's PSNR is" % n, PSNR)
    print(PSNRList)
    print(MseList)
    plt.title("PSNR-Bitrate Figure", fontsize=22)
    plt.xlabel("Bitrate(Kb/sec)", fontsize=12)
    plt.ylabel("PSNR", fontsize=22)
    plt.plot(Bitrate, PSNRList, color="blue", linewidth=3, marker="o", markersize=5,
             markerfacecolor="red")

    plt.show()


def drawDiffR():
    for n in range(2, 7):
        Mse, MsePerFrameList = MSE(2, n, width, height)
        MsePerFrameListLarge.append(MsePerFrameList)
    plt.title("MSE-FrameNo", fontsize=22)
    plt.xlabel("FrameNo", fontsize=12)
    plt.ylabel("MSE", fontsize=22)

    plt.plot(FrameNo, MsePerFrameListLarge[0], color="blue", label='2000 bits/s', linewidth=1, marker="o", markersize=1,
             markerfacecolor="red")
    plt.plot(FrameNo, MsePerFrameListLarge[1], color="green", label='3000 bits/s', linewidth=1, marker="o",
             markersize=1,
             markerfacecolor="red")
    plt.plot(FrameNo, MsePerFrameListLarge[2], color="yellow", label='4000 bits/s', linewidth=1, marker="o",
             markersize=1,
             markerfacecolor="red")
    plt.plot(FrameNo, MsePerFrameListLarge[3], color="red", label='5000 bits/s', linewidth=1, marker="o", markersize=1,
             markerfacecolor="red")
    plt.plot(FrameNo, MsePerFrameListLarge[4], color="black", label='6000 bits/s', linewidth=1, marker="o",
             markersize=1,
             markerfacecolor="red")
    plt.legend()

    plt.savefig(r'F:\Master\NTU\6427-Video Signal Process\Assignment\FrameMse', dpi=300)
    plt.show()

if __name__ == '__main__':
    width = 352
    height = 288
    MseList = list()
    PSNRList = list()
    MsePerFrameListLarge = list()
    FrameNo = list(range(1, 151))

    Mse, MsePerFrameList = MSE(1, 2, width, height)
    MsePerFrameListLarge.append(MsePerFrameList)

    plt.title("MSE-FrameNo", fontsize=22)
    plt.xlabel("FrameNo", fontsize=12)
    plt.ylabel("MSE", fontsize=22)

    plt.plot(FrameNo, MsePerFrameListLarge[0], color="blue", label='2000 bits/s', linewidth=1, marker="o", markersize=1,
             markerfacecolor="red")
    plt.savefig(r'F:\Master\NTU\6427-Video Signal Process\Assignment\ask', dpi=300)

    plt.show()
    #drawDiffR()
