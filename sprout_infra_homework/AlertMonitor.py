import logging
import json
import sys
import collections


class AlertMonitor:
    """ Class to monitor & alert on specific criteria listed below:
    -  Send an alert when any server's `DiskUsedPercentage` component exceeds 0.9 (90%). Do not alert for inactive servers.
    - Send an alert when the majority of servers within a service exhibit `Load5mAvg` with a value greater than 4.0 at the same time. Do not include inactive servers when calculating majority.
    """

    def __init__(self):
        self.alert_list = []

    def set_application_logger(self):
        """
        Method to set logger for this application. This is to be used to troubleshoot issues with this application.

        Args: None
        Returns: None
        """
        logger = logging.getLogger('alertMonitor_logger')
        logger.setLevel(logging.ERROR)
        handler = logging.StreamHandler()
        handler.setLevel(logging.ERROR)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        self.logger = logger


    def set_metric_file(self, metric_file):
        """
        Method to set the metric file that will be parsed for alerting

        Args: metric_file
        Returns: None
        """
        try :
            with open(metric_file, "r") as read_file:
                self.metric_data = json.load(read_file)  
        except Exception as error:
            self.logger.error("Error while opening metric_file. Please review error: %s" % error)

    def disk_usage_alerter(self, alert_threshold):
        """
        Method to alert if DiskUsagedPercentage exceed alert_threshold
        Do not alert for inactive conditions

        Args: alert_threshold
        Returns: None
        """
        try :
            for metric in self.metric_data:
                if "component" in metric:
                    if metric['component'].lower() == "DiskUsedPercentage".lower():
                        if(metric['active']):
                            if (metric['value'] > alert_threshold):
                                self.alert_list.append(metric)
        except Exception as error:
            self.logger.error("Error while getting disk usage alert. Please review error: %s" % error)

    def load_avg_alerter(self, alert_threshold):
        """
        Method to alert if the majority of servers within a service exhibit "Load5mAvg" with a value greater alert_threshold at the same time
        Do not include inactive servers when calclating majority

        Args: alert_threshold
        Returns: None
        """
        try:
            list_split_result = collections.defaultdict(list)
            for metric in self.metric_data:
                list_split_result[metric['service']].append(metric)
            result_list = list(list_split_result.values())
            for result in result_list:
                half = len(result) / 2
                thresholdActiveValueList = [d for d in result if d['active'] and d['value'] > alert_threshold]
                if (len(thresholdActiveValueList) > half):
                    for entry in thresholdActiveValueList:
                        self.alert_list.append({'clusterd_service': True, 'timestamp': entry['timestamp'], 'component': entry['component'], 'value': alert_threshold, 'service': entry['service'] })
        except Exception as error:
            self.logger.error("Error while getting load average alert. Please review error: %s" % error)

    def alert_output(self):
        """
        Method to output alert if any found

        Args: None
        Returns: None
        """
        try:
            if (self.alert_list):
                for alert in self.alert_list:
                    if ('clusterd_service' in alert):
                        print("ALERT timestamp: %s, component: %s, value: %s, service: %s" % (alert['timestamp'], alert['component'], alert['value'], alert['service']))
                    else:
                        print("ALERT timestamp: %s, component: %s, value: %s, server: %s, service: %s" % (alert['timestamp'], alert['component'], alert['value'], alert['server'], alert['service'])) 
        except Exception as error:
            self.logger.error("Error while outputting alert_output. Please review error: %s" % error)


if __name__ == "__main__":
    # get metric.json
    if not sys.argv[1:]:
        print('\nYou must pass the metric.json file\n Example: python3 AlertMonitor.py metric.json')
        sys.exit(1)
    
    metric_file = sys.argv[1]

    # start application
    alertMonitor = AlertMonitor() 

    # set application logger
    alertMonitor.set_application_logger()

    # set metric_file
    alertMonitor.set_metric_file(metric_file)

    # trigger alert if diskUsagePercentage exceeds 90%
    alertMonitor.disk_usage_alerter(alert_threshold=0.9)

    # trigger alert on load_avg
    alertMonitor.load_avg_alerter(alert_threshold=4.0)

    # printing alert
    alertMonitor.alert_output()
