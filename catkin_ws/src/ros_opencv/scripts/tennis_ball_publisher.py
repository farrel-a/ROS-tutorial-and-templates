import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import sys

bridge = CvBridge()
if __name__ == '__main__':
    rospy.init_node("tennis_ball_publisher",anonymous=True)
    video_capture = cv2.VideoCapture('/home/farrel/catkin_ws/src/ros_opencv/video/tennis-ball-video.mp4')
    image_pub = rospy.Publisher("/tennis_ball_image",Image, queue_size=100)
    loop_rate = rospy.Rate(30)

    while (True):
        ret, frame = video_capture.read()
        img_msg = bridge.cv2_to_imgmsg(frame,"bgr8")
        image_pub.publish(img_msg)
        loop_rate.sleep()
