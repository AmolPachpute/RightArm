from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from thumbs import ImageWithThumbsField
from ckeditor.fields import RichTextField
import datetime
from Member.models import Base, Member
from django.contrib.auth import login
from ckeditor.fields import RichTextField

# Create your models here.

RELATION_CHOICES = ( ('Removed', 'Removed'), ('Pending', 'Pending'), ('Connected', 'Connected'))

MESSAGE_STATUS_CHOICES = [('Inbox', 'Inbox'), ('Sent', 'Sent'), ('Trash', 'Trash')]


class Like(Base):

    like = models.BooleanField(default=True)
    liked_by = models.ForeignKey(Member, related_name='Liked_By_Member')
    description = models.CharField('Description', blank=True, null=True,
                                   max_length=300)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name='LikeCTPM')
    object_id = models.TextField(_('object ID'))
    relatedTo = generic.GenericForeignKey(ct_field='content_type',
            fk_field='object_id')

    def __unicode__(self):
        return self.liked_by



class Share(Base):

    shared_by = models.ForeignKey(Member, related_name='Shared_By_Member')
    description = models.CharField('Description', blank=True, null=True,
                                   max_length=300)
    content_type = models.ForeignKey(ContentType,
                                     verbose_name=_('content type'),
                                     related_name='ShareCTPM')
    object_id = models.TextField(_('object ID'))
    relatedTo = generic.GenericForeignKey(ct_field='content_type',
            fk_field='object_id')

    def __unicode__(self):
        return self.shared_by.user.first_name


class ConversationRelation(Base):

    """ ConversationRelation """

    member1 = models.ForeignKey(Member, blank=True, null=True,
                                related_name='Sender')
    member2 = models.ForeignKey(Member, blank=True, null=True,
                                related_name='Receiver')

    class Meta:

        verbose_name_plural = 'Conversation Relation'

    def __unicode__(self):
        return '%s - %s' % (self.member1.user.first_name,
                            self.member2.user.first_name)

    def get_conversations(self):
        return Conversations.objects.filter(is_active=True, message=self)


class Conversations(models.Model):

    """ Conversations """

    message = models.ForeignKey(ConversationRelation)
    body = models.TextField(blank=True, null=True)
    member = models.ForeignKey(Member, blank=True, null=True,
                               related_name='Senderrss')
    created = models.DateTimeField(verbose_name=_('Created at'),
                                   auto_now_add=True)
    seen = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    status = models.IntegerField(choices=MESSAGE_STATUS_CHOICES, default=0,
                                 null=True)

    class Meta:

        verbose_name_plural = 'Conversations'

    def __unicode__(self):
        return '%s - %s' % (self.message.member1.user.first_name,
                            self.message.member2.user.first_name)


class Refer_Friend(models.Model):

    referred = models.ForeignKey(Member, blank=True, null=True)
    friend_name = models.CharField(max_length=40)
    friend_email = models.EmailField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    is_registered = models.BooleanField(default=False, blank=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s ' % self.referred.user.first_name

class Refer_Friend_Userdata(models.Model):

    referrer = models.ForeignKey(Refer_Friend)
    friend_email = models.CharField(max_length=40)
    hash_value = models.CharField(max_length=80)
    is_done = models.BooleanField(default=False, blank=True)

    def __unicode__(self):
        return '%s - %s' % (self.referrer.referred, self.friend_email)

class MemberRelation(Base):

    """ MemberRelation for connections between 2 members i.e friend, not a friend or request pending, etc"""

    relation_type = models.CharField(max_length=100, choices=RELATION_CHOICES, default='Removed',
            verbose_name='Relation Type*')
    from_id = models.ForeignKey(Member, related_name='FromID',
                                verbose_name='From Id*')
    to_id = models.ForeignKey(Member, related_name='ToId',
                              verbose_name='To Id*')
    unfriend = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s %s %s' % (self.relation_type, self.from_id, self.to_id)

class MemberSuggestion(Base):

    """ MemberRelation """

    from_id = models.ForeignKey(Member, related_name='From',
                                verbose_name='From Id*')
    to_id = models.ForeignKey(Member, related_name='To', verbose_name='To Id*'
                              )
    suggested_members = models.ManyToManyField(Member,
            related_name='Suggested Members', blank=True, null=True)

    def __unicode__(self):
        return u'%s - %s' % (self.self.from_id, self.to_id)

class GroupChat(Base):

    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(Member, related_name='Created By')
    participants = models.ManyToManyField(Member, related_name='Group Members')

    def __unicode__(self):
        return self.name

class GroupChat_Conversations(models.Model):

    text = models.TextField()
    sender = models.ForeignKey(Member)
    thread = models.ForeignKey(GroupChat)
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)

    def __unicode__(self):
        return '%s' % self.sender.user.first_name

msg_type_choices = (('sent', 'sent'),('received', 'received'), )
status = (('success', 'success'), ('failure', 'failure'))

class Messages(Base):

    profile = models.ForeignKey(Member, related_name='profile')
    subject = models.CharField(max_length=200)
    msg_from = models.ForeignKey(Member, related_name='Message From', verbose_name='Message From*')
    msg_to = models.ForeignKey(Member, related_name='Message To', verbose_name='Message To*')
    message = RichTextField(verbose_name="Message*")
    seen = models.BooleanField(default=False)
    seen_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(choices=status, max_length=200)
    msg_type = models.CharField(choices=msg_type_choices, max_length=200)
    delivered_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return '%s -> %s' % (self.msg_from.user.first_name, self.msg_to.user.first_name)

    def get_attachment(self):
        try:
            return Attachments.objects.filter(content_type=ContentType.objects.get_for_model(Messages), object_id=self.id)
        except:
            return ''

class Attachments(Base):

    ''' attachment  can be for message or for chat so using content types '''

    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    related_to = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")
    image_attachment = ImageWithThumbsField(upload_to = 'static/%Y/%m/%d', sizes=((90, 120), (180, 240), (360, 480)), blank=True, null=True )
    file_attachment = models.FileField(upload_to='static/%Y/%m/%d', blank=True, null=True)
