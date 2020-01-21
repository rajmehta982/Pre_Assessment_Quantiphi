import boto3
import time
region = 'us-east-1'
instances = ['i-0e23c685ff55c2f84']
ec2 = boto3.client('ec2', region_name=region)

ec2.start_instances(InstanceIds=instances)
print('started your instances: ' + str(instances))

time.sleep(180)

ec21 = boto3.resource('ec2', region_name=region)
instance = ec21.Instance('i-0e23c685ff55c2f84')
volumes = instance.volumes.all()

for v in volumes:
    print("Your volume-id is: " + v.id)


volumes_dict = {
                  'raj-snap-1' : 'vol-09d08b4e14e9eee73',
                  
          }
# create a dictionary of snapshots with their snapshot ids which were created successfully
successful_snapshots = dict()
# iterate through each item in volumes_dict and use key as description of snapshot
for snapshot in volumes_dict:
    try:
        response = ec2.create_snapshot(
            Description= snapshot,
            VolumeId= volumes_dict[snapshot],
            DryRun= False
        )
        # response is a dictionary containing ResponseMetadata and SnapshotId
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        snapshot_id = response['SnapshotId']
        # check if status_code was 200 or not to ensure the snapshot was created successfully
        if status_code == 200:
            successful_snapshots[snapshot] = snapshot_id
    except Exception as e:
        exception_message = "There was error in creating snapshot " + snapshot + " with volume id "+volumes_dict[snapshot]+" and error is: \n"\
                            + str(e)
# print the snapshots which were created successfully
print(successful_snapshots)

time.sleep(180)


ec2.stop_instances(InstanceIds=instances)
print('stopped your instances: ' + str(instances))

time.sleep(180)

ec2.terminate_instances(InstanceIds=instances)
print('terminated your instances: ' + str(instances))


