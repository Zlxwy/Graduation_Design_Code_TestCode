import threading
import serial
import queue
import time

"""
一个用于异步串口通信的类，支持多线程安全的发送和接收。
"""
class UartStream:

  """
  初始化串口连接和内部组件。
  Args:
      port (str): 串口设备路径，例如 "/dev/ttyS1"。
      baudrate (int, optional): 波特率，默认 115200。
      bytesize (int, optional): 数据位，默认 8 位。
      parity (str, optional): 校验位，默认无校验。
      stopbits (int, optional): 停止位，默认 1 位。
  """
  def __init__(self,
              port="/dev/ttyS1", 
              baudrate=115200,
              bytesize=serial.EIGHTBITS, 
              parity=serial.PARITY_NONE,
              stopbits=serial.STOPBITS_ONE):
    self.uart = serial.Serial(
      port=port,
      baudrate=baudrate,
      bytesize=bytesize,
      parity=parity,
      stopbits=stopbits
    )

    self._send_queue = queue.Queue() # 发送队列，用于多线程安全地传递待发送数据
    self._writer_thread = None # 发送线程，负责从队列中获取数据并发送
    self._running = False # 运行标志，用于控制发送线程是否继续运行



  """
  启动内部的发送线程，开始处理发送队列。
  """
  def Start(self):
    if self._running: # 如果线程已经在运行（可能是因为重复调用了）
      return # 直接返回，避免重复启动线程
    self._running = True # 设置运行标志为 True，开始运行发送线程
    self._writer_thread = threading.Thread(  # 创建专门的发送线程对象
      target=self._serial_writer_worker,  # 设置目标函数为 _serial_writer_worker
      daemon=True # 设置为守护线程，确保在主线程退出时自动结束
    )
    self._writer_thread.start()  # 启动发送线程



  """
  停止串口流，关闭线程和串口连接。
  # Args:
    timeout (float, optional): 等待线程结束的超时时间（秒）。
  """
  def Stop(self, timeout=2):
    if not self._running: # 如果线程不在运行（可能是因为没有调用 Start()）
      return # 直接返回，避免重复停止线程
    self._running = False # 设置运行标志为 False，停止发送线程
    self._send_queue.put(None) # 发送退出信号(None)给发送线程
    if self._writer_thread and self._writer_thread.is_alive(): # 如果发送线程还存在，并且还在运行
      self._writer_thread.join(timeout=timeout) # 等待线程结束，最多等待 timeout 秒
    self.uart.close() # 关闭串口连接



  """
  专门的发送线程工作函数，是唯一调用 ser.write() 的地方。
  """
  def _serial_writer_worker(self):
    while self._running:
      try:
        data_to_send = self._send_queue.get(timeout=1) # 从队列中获取要发送的数据 (阻塞式)
        if data_to_send is None: # 如果收到退出信号(None)
          self._send_queue.task_done() # 标记任务完成
          break # 退出循环，结束发送线程
        bytes_written = self.uart.write(data_to_send) # 执行实际的串口发送
        self.uart.flush() # 确保数据被发送出去
        print(f"UART: Sent {bytes_written} bytes: {repr(data_to_send)}") # 打印发送信息
        self._send_queue.task_done() # 标记队列中的这个任务已经完成
          
      except queue.Empty: # 超时没检测到队列数据
        continue # 队列为空，继续循环检查 self._running 状态

      except Exception as e: # 其他异常
        print(f"Error in UART writer thread: {e}") # 打印异常信息
        if data_to_send is not None: # 如果队列中还有数据
          self._send_queue.task_done() # 发生错误时也应标记任务完成，以防队列卡住



  """
  将数据加入发送队列，由后台线程异步发送。
  这个方法是线程安全的，可以被多个线程同时调用。
  Args:
    data (str): 要发送的字符串数据。
  """
  def SendString(self, strdata: str):
    if not self._running:  # 如果线程不在运行（可能是因为没有调用 Start()）
      raise RuntimeError("UART Stream is not running. Cannot send data.") # 抛出运行时错误，提示用户先启动 UartStream
    self._send_queue.put(strdata.encode('utf-8')) # 将字符串放入队列，由发送线程处理

  def SendArray(self, arrdata: bytearray):
    if not self._running:  # 如果线程不在运行（可能是因为没有调用 Start()）
      raise RuntimeError("UART Stream is not running. Cannot send data.") # 抛出运行时错误，提示用户先启动 UartStream
    self._send_queue.put(arrdata) # 将字符串放入队列，由发送线程处理

