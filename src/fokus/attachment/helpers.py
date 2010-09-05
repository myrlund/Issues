from datetime import datetime

def get_upload_path(instance, filename):
    """ Returns context-dependent upload path """
    
    # Assuming instance is the attachment model
    print "INSTANCE: " + str(instance.attached_to.all())
    return instance.attached_to.parent.get_upload_path(filename)

def generate_filename(instance, filename):
    print "Generating filename: ",
    return "images/%s-%s" % (datetime.now().strftime("%Y/%m/%d/%H%M"), filename)
