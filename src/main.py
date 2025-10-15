import sys
import time


def main():
    print("starting main...")
    #scrape and save to mongodb
    import storage
    
    time.sleep(2)
    
    #etl to hdfs
    import etl_to_hdfs
    time.sleep(2)
    #spark analytics
    import spark_script
    print("done all steps")
    return

if __name__ == "__main__":
    main()
    