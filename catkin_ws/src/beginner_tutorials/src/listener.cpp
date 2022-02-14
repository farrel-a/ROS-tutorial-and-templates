#include "ros/ros.h"
#include "std_msgs/String.h"

void chatterCallback (const std_msgs::String::ConstPtr& msg)
{
    ROS_INFO("I heard : [%s]", msg->data.c_str());
}

int main(int argc, char **argv)
{
    //initialize ros
    ros::init (argc, argv, "listener");

    //intialize node
    ros::NodeHandle nh;

    //call ros to subscribe a topic
    ros::Subscriber sub = nh.subscribe("chatter", 1000, chatterCallback); //([topic name], queue, funcrtion call)

    //loop for pumping callbacks
    ros::spin(); 

    return 0;
}