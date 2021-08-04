#!/usr/bin/env python

# import mysql.connector
import pymysql
import rospy
from geometry_msgs.msg import PoseStamped
import time
from rosgraph_msgs.msg import Log

def callback(data):
    global pub
    global sub
    global cnt
    global bed_count
    if data.msg == "Got new plan":
        print(data.msg)
    elif data.msg == "Goal reached":
        print(data.msg)
        print("THE END")
        sub.unregister()
        cnt += 1
        if cnt != bed_count:
            set_goal()
            
def set_goal():
    global pub
    global sub
    global cnt
    pub = rospy.Publisher("/move_base_simple/goal", PoseStamped, queue_size=1)

    stamp = PoseStamped()
    stamp.header.seq=10
    stamp.header.frame_id = 'map'
    print(time.gmtime(time.time()))
    stamp.pose.position.x = bed_location[cnt][0]
    stamp.pose.position.y = bed_location[cnt][1]
    stamp.pose.position.z = 0.0
    stamp.pose.orientation.x = 0.0
    stamp.pose.orientation.y = 0.0
    stamp.pose.orientation.z = bed_location[cnt][2]
    stamp.pose.orientation.w = bed_location[cnt][3]
    rospy.sleep(1)
    pub.publish(stamp)
    pub.unregister()


    sub = rospy.Subscriber("/rosout", Log, callback)
    rospy.spin()

if __name__ == "__main__":
    rospy.init_node('go')

    pub = None
    sub = None
    sql = "select x,y,z,w from bed"
    cnt = 0

    conn = pymysql.connect(host='13.125.218.224', port=3306, database='rest_api', user='test', password='test', charset='utf8')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    
    bed_count = len(cursor.fetchall())
    bed_location = [(0.0, 0.0, 0.0, 0.0) for _ in range(bed_count)]
    
    cursor.execute(sql)

    for i, row in enumerate(cursor):
        bed_location[i] = (row['x'], row['y'], row['z'], row['w'])

    set_goal()
