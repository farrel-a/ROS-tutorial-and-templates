#include <ros/ros.h>
#include <ros_service_assignment/RectangleAreaService.h>
#include <ros_service_assignment/RectangleAreaServiceRequest.h>
#include <ros_service_assignment/RectangleAreaServiceResponse.h>

bool area(ros_service_assignment::RectangleAreaService::Request &req,
          ros_service_assignment::RectangleAreaService::Response &res)
{
    res.area = req.width*req.height;
    ROS_INFO("Request : Width = %.2f , Height = %.2f", req.width, req.height);
    ROS_INFO("Area = %f", res.area);
    return true;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "rectangle_server");
    ros::NodeHandle nh;

    ros::ServiceServer service = nh.advertiseService("/rectangle_area", area);
    ROS_INFO("Ready to calculate rectangle area");
    ros::spin();

    return 0;
}