#include <ros/ros.h>
#include <ros_service_assignment/RectangleAreaService.h>
#include <ros_service_assignment/RectangleAreaServiceRequest.h>
#include <ros_service_assignment/RectangleAreaServiceResponse.h>

int main (int argc, char **argv)
{
    ros::init(argc,argv,"rectangle_client");
    ros::NodeHandle nh;
    ros::ServiceClient client = nh.serviceClient<ros_service_assignment::RectangleAreaService>("/rectangle_area");

    ros_service_assignment::RectangleAreaService srv;
    srv.request.width = atoll(argv[1]);
    srv.request.height = atoll(argv[2]);

    ROS_INFO("Requested : Width = %.2f, Height = %.2f", srv.request.width, srv.request.height);
    
    client.call(srv);

    ROS_INFO("Area : %.2f * %.2f = %.2f", srv.request.width, srv.request.height, srv.response.area);
    
    return 0;

}