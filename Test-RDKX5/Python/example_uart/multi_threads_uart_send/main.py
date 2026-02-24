from Timer import Timer
from UartStream import UartStream
import time





s
def send_hello(): # 通过串口发送 Hello! 的函数
  MainCmnct.SendString( f"[{time.strftime('%H:%M:%S')}] Hello!\n" )

def send_hi(): # 通过串口发送 Hi! 的函数
  MainCmnct.SendString( f"[{time.strftime('%H:%M:%S')}] Hi!\n" )

def send_array(): # 通过串口发送数组的函数
  MainCmnct.SendArray( bytearray([0x66, 0x67, 0x68, 0x69, 0x6A, ord('\n')]) ) # 调用 UartStream 实例的 SendArray 方法发送数组





MainCmnct = UartStream(port="/dev/ttyS1", baudrate=115200) # 创建 UartStream 实例
MainCmnct.Start() # 启动 UartStream 实例
print("UartStream started") # 打印 UartStream 实例已启动信息

timer_hello = Timer(interval_ms=500, task=send_hello) # 1000ms间隔调用send_hello
timer_hi = Timer(interval_ms=3000, task=send_hi) # 3000ms间隔调用send_hi
timer_array = Timer(interval_ms=5000, task=send_array) # 5000ms间隔调用send_arra
timer_hello.start()  # 启动 timer_hello 定时器
print("timer_hello started")  # 打印 timer_hello 定时器已启动信息
timer_hi.start()  # 启动 timer_hi 定时器
print("timer_hi started")  # 打印 timer_hi 定时器已启动信息
timer_array.start()  # 启动 timer_array 定时器
print("timer_array started")  # 打印 timer_array 定时器已启动信息

try:
  while True: pass  # 主循环，保持程序运行

except KeyboardInterrupt: # 捕获键盘中断异常
  print("\nCaught KeyboardInterrupt, stopping timers...")

finally:
  timer_hello.stop()  # 停止 timer_hello 定时器
  print("timer_hello stopped")  # 打印 timer_hello 定时器已停止信息
  timer_hi.stop()  # 停止 timer_hi 定时器
  print("timer_hi stopped")  # 打印 timer_hi 定时器已停止信息
  timer_array.stop()  # 停止 timer_array 定时器
  print("timer_array stopped")  # 打印 timer_array 定时器已停止信息

  MainCmnct.Stop()  # 停止 UartStream 实例
  print("UartStream stopped")  # 打印 UartStream 实例已停止信息

  print("\nTimers and UartStream have been stopped!")
  print("Main program has been terminated!")
