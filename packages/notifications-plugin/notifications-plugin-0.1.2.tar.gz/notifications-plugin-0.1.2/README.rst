Notifications Plugin
====================

Introduction
============

A Django app to create notifications

Requirements
============

- Python 3.5, 3.6, 3.7, 3.8
- Django 2.2, 3.0

Installation
============

Install the app using pip

::

    $ pip install notifications-plugin


or get it from source

::

    $ git clone https://github.com/adityacp/notifications_plugin.git
    $ cd notifications_plugin
    $ python setup.py sdist
    $ pip install dist/notifications_plugin*


Add the django app to your Project
    
::

    INSTALLED_APPS = (
        'django.contrib.auth',
        ...
        'notifications_plugin',
        ...
    )


To run schema migration, execute ``python manage.py makemigrations notifications_plugin`` and then run ``python manage.py migrate``.

Creating Notifications
======================

QuerySet methods
~~~~~~~~~~~~~~~~

* *Create Single notification message*

  To add an notification message, simply import the NotificationMessage model from the notifications_plugin app.

  ::

      from notifications_plugin.models import NotificationMessage

      NotificationMessage.objects.add_single_message(creator_id, summary, description, msg_type)

  Arguments:
  
  * **creator_id**: An user's id who is creating the message.
  * **summary**: A summary of the message
  * **description**: A description of the actual message
  * **msg_type**: Message Type i.e. whether it is informational message, danger message, success message or warning message.     Default is the informational message (info).
    
    ``Available message types are info, danger, warning, success.``

* *Create Bulk notification Message*

  ::

      NotificationMessage.objects.add_bulk_messages(messages)

  Arguments:

  * **messsages**: A list of dictionaries containing the following values. Sample messages list is as follows
    
    ``messages = [{"creator_id" : 1, "summary" : "test", "description": "test description", "message_type": "info"}]``
 
* *Create notifications*

  * To create notification for multiple receivers with single message
  
    ::

        from notifications_plugin.models import Notification

        Notification.objects.add_bulk_user_notifications(receiver_ids, msg_id)

    Arguments:
     
    * **receiver_ids**: A list of receiver ids to whom the notification is to be sent
    * **msg_id**: A NotificationMessage id which will be sent to the receivers

  * To create notification for single receiver with multiple messages
  
    ::
        
        Notification.objects.add_bulk_msg_notifications(receiver_id, msg_ids)
  
  
  * To create notification for single receiver with single message
  
    ::
    
        Notification.objects.add_single_notification(receiver_id, msg_id)

* *Getting and Marking Notifications*

  * To mark notifications for multiple receivers with single message
  
    ::
    
       Notification.objects.mark_bulk_user_notifications(receiver_ids, msg_uuid, read)
    
    Arguments:
    
    * **receiver_ids**: A list of receiver ids to whose notification is to be marked
    * **msg_id**: A NotificationMessage uuid(unique identifier) whose message is supposed to be marked. To get the uuid of the message just type ``message.uid``
    * **read**: Indicates if the message for the particular receiver is marked or not. Default is `False`. To mark as read, make it `True`.

  * To mark notifications for single receiver with multiple messages
  
    ::

        Notification.objects.mark_bulk_msg_notifications(receiver_id, msg_uuids, read)
  
  * To mark notification for single receiver with single message
  
    ::
    
        Notification.objects.mark_single_notification(receiver_id, msg_uuid, read)
  
  * To get a particular receiver's all notifications
  
    ::
    
        Notification.objects.get_receiver_notifications(receiver_id)
  
  * To get unread notifications of a particular receiver
  
    ::
    
        Notification.objects.get_unread_receiver_notifications(receiver_id)

  * To get read notifications of a particular receiver
  
    ::
    
        Notification.objects.get_read_receiver_notifications(receiver_id)
  
  * To get multiple receivers notifications
  
    ::
    
        Notification.objects.get_multiple_user_notifications(receiver_ids)
  
  * To get notifications by a specific message
  
    ::
    
        Notification.objects.get_notifications_by_msg(msg_uuid)

Issues
======

If you find any issues or want a specific functionality, please file a issue here:
https://github.com/adityacp/notifications_plugin/issues/new/choose

