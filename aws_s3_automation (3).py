# First, we need to import the boto3 library so we can use AWS services
import boto3

# Alright, let's get started by connecting to AWS S3
# We'll create an S3 resource and specify the region where our bucket will live
s3 = boto3.resource('s3', region_name='ap-northeast-2')

# Now, let's give our bucket a name
bucket_name = '1-boto3-buck'


# ================================
# CHECK IF THE BUCKET EXISTS (CREATE IF NOT)
# ================================
# Time to see if the bucket already exists
# We'll list all the buckets in our AWS account and store their names in a list
all_my_buckets = [bucket.name for bucket in s3.buckets.all()]

# If our bucket isn't in the list, let's create it
if bucket_name not in all_my_buckets:
    print(f"Looks like '{bucket_name}' doesn't exist. Let's create it!")

    # Creating the bucket using the name and region
    s3.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'ap-northeast-2'
        }
    )

    print(f"Bucket '{bucket_name}' is now ready to go!")
else:
    print(f"Bucket '{bucket_name}' already exists. No need to make another one.")


# ================================
# FILES TO WORK WITH
# ================================
# We've got two files to play with: one to upload and another to update the first one
file_1 = 'file_1.txt'
file_2 = 'file_2.txt'


# ================================
# UPLOAD A FILE TO S3
# ================================
# Let's upload 'file_1.txt' to our shiny new bucket
print("\nUploading 'file_1.txt' to S3...")

s3.Bucket(bucket_name).upload_file(Filename=file_1, Key=file_1)

print(f"All done! '{file_1}' is now chilling in the bucket '{bucket_name}'.")


# ================================
# READ AND PRINT FILE CONTENT FROM S3
# ================================
# Let's make sure we can read the file we just uploaded
print("\nReading the content of 'file_1.txt' from S3...")

# Grab the file from S3 using its name
obj = s3.Object(bucket_name, file_1)

# Read the content of the file (it'll come as bytes, so we'll decode it)
body = obj.get()['Body'].read()
print("Here's what 'file_1.txt' says:", body.decode('utf-8'))


# ================================
# UPDATE THE FILE IN S3
# ================================
# Now let's update the content of 'file_1.txt' with what's inside 'file_2.txt'
print("\nUpdating 'file_1.txt' with the content of 'file_2.txt'...")

# Open 'file_2.txt' in binary mode and upload it to replace 'file_1.txt'
s3.Object(bucket_name, file_1).put(Body=open(file_2, 'rb'))

print("Update complete! Let's see what 'file_1.txt' says now.")

# Read and print the updated content
obj = s3.Object(bucket_name, file_1)
body = obj.get()['Body'].read()
print("Updated content of 'file_1.txt':", body.decode('utf-8'))


# ================================
# DELETE FILE FROM S3
# ================================
# Time to clean up by deleting 'file_1.txt' from the bucket
print("\nDeleting 'file_1.txt' from the bucket...")

s3.Object(bucket_name, file_1).delete()

print("'file_1.txt' is now gone from the bucket.")


# ================================
# DELETE THE BUCKET
# ================================
# Finally, let's delete the bucket itself (it has to be empty first)
print("\nDeleting the bucket...")

bucket = s3.Bucket(bucket_name)
bucket.delete()

print(f"Bucket '{bucket_name}' has been deleted. All done!")
