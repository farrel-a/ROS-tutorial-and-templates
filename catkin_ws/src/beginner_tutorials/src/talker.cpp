#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>

int main(int argc, char **argv)
{
    //ros::init(argc, argv, [node name])
    ros::init(argc, argv, "talker"); 

    //node handle is to initialize node so that the node can communicate within ROS system
    ros::NodeHandle nh; 

    ros::Publisher chatter_pub = nh.advertise<std_msgs::String>("chatter", 1000); //([topic name], queue)

    ros::Rate loop_rate(10); //10 Hz

    int count = 0; //counter how many messages that have been sent

    while (ros::ok())
    {
        std_msgs::String msg;

        std::stringstream ss;
        ss<<"hello world"<<count;
        msg.data = ss.str();
        ROS_INFO("%s", msg.data.c_str());
        chatter_pub.publish(msg);
        
        ros::spinOnce();

        loop_rate.sleep();
        count++;
    }
    
    return 0;
}