import cv2

def main():
  cap = cv2.VideoCapture(0) # 创建摄像头捕获对象，0表示默认摄像头
  if not cap.isOpened(): # 如果摄像头未成功打开
    print("无法打开摄像头") # 打印错误信息
    return # 退出程序
  
  cv2.namedWindow('cam') # 创建名为"cam"的窗口
  print("按ESC键退出程序")
  while True:
    ret, frame = cap.read() # 读取摄像头帧
    if not ret: # 如果帧读取失败
      print("无法读取摄像头帧")  # 打印错误信息
      break # 退出循环
    cv2.imshow('cam', frame) # 在窗口中显示帧
    if cv2.waitKey(1) & 0xFF == 27:  # 如果按下ESC键
      break # 退出循环
    
  cap.release() # 释放摄像头
  cv2.destroyAllWindows() # 关闭所有窗口

if __name__ == "__main__":
  main()
