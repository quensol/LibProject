
import cv2
import pyzbar.pyzbar as pyzbar


def zbar_demo():
    img = cv2.imread(r'app/static/image/10007.jpg')
    zbars = pyzbar.decode(img)

    order = 1
    if zbars:
        for item in zbars:
            txt = item.data.decode('utf-8')

            x, y, w, h = item.rect
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

            txt_show = "{0}  {1}  {2}-{3}".format(str(order), txt, x, y)
            cv2.putText(img, txt_show, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 125), 2)
            order = order + 1
            print(item)
    cv2.imshow('zbar_demo', img)
    cv2.waitKey(0)


if __name__ == '__main__':
    zbar_demo()