# FWaaS test performance with Netlink
## This repo describes the FWaaS test performance using Netlink to delete conntrack entries

1. Calculate time deleting conntrack entries with current solution (conntrack-tools)

  1.1. Apply the diff file:
    > File: time_calculate.diff
    
    > Go to repo (ex. /opt/stack/neutron-fwaas/)

    > patch -p1 < /directory/to/file

  1.2. Observe log file
    > tail -f /opt/stack/q-l3.log | grep "FWaaSNetlink"
  
  1.3. Run the test scripts
    > (1) Create Firewall rules

    >> python create_rules.py <start_rule> <end_rule>
    
    >> start_rule: rule source_port start number, end_rule: rule source_port end number
    
    >> start_rule should be equal START_RULE in test_performance.py
    
    > (2) Test performance
    
    >> python test_performance.py
    
    > ``Note: To run test performance again, we only need to run step (2)`` 

2. Calculate time deleting conntrack entries with Netlink solution
  
  2.1. Apply the patch
    > Clone & apply patch: https://review.openstack.org/#/c/389654/
  
  2.2. Apply the diff file
    > File: time_calculate_2.diff
  
  2.3 Observe log file
    > tail -f /opt/stack/q-l3.log | grep "FWaaSNetlink"
  
  2.4. Run the test scripts
    > (1) Create Firewall rules
    
    >> python create_rules.py <start_rule> <end_rule>
    
    >> start_rule: rule source_port start number, end_rule: rule source_port end number

    >> start_rule should be equal START_RULE in test_performance.py
    
    > (2) Test performance
    
    >> python test_performance.py
    
    > ``Note: If we already have firewall rules (already run *create_rules.py*, run step (2) only``

3. Experimental log
   https://github.com/uttu90/FWaaSNetlink/blob/master/experimental_log.txt is a log from my test.
