"""
File for setup the custom Queryset, Manager and model for soft delete feature
"""
from django.db import models
from django.utils import timezone


class BaseQuerySet(models.QuerySet):
	"""
	Create custom query for soft delete operation support
	"""

	def delete(self):
		"""
		Applies sof delete over query objects.
		:return: Queryset with update operation over deleted_at field.
		"""
		return super(BaseQuerySet, self).update(deleted_at=timezone.now())

	def force_delete(self):
		"""
		Delete the record from the database.
		:return: Queryset with normal delete operation.
		"""
		return super(BaseQuerySet, self).delete()


class BaseManager(models.Manager):
	"""
	Provides a Manager to handle Query Sets and manage soft deleting
	"""

	def __init__(self, *args, **kwargs):
		self.include_deleted = kwargs.pop('include_deleted', False)
		self.only_deleted = kwargs.pop('only_deleted', False)
		super(BaseManager, self).__init__(*args, **kwargs)

	def get_queryset(self):
		if self.only_deleted:
			return BaseQuerySet(self.model).exclude(deleted_at=None)
		if not self.include_deleted:
			return BaseQuerySet(self.model).filter(deleted_at=None)
		return BaseQuerySet(self.model)

	def force_delete(self):
		return self.get_queryset().force_delete()


class BaseModel(models.Model):
	"""
	The base model for all objects in th project
	"""
	# Setup the manager
	objects: BaseManager = BaseManager()
	all_objects = BaseManager(include_deleted=True, only_deleted=False)
	deleted_objects = BaseManager(only_deleted=True, include_deleted=False)

	# Declare attributes
	id = models.BigAutoField(primary_key=True, auto_created=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	deleted_at = models.DateTimeField(blank=True, null=True, editable=False)

	# Custom functions for delete and sof delete
	def delete(self, using=None, keep_parents=False):
		self.deleted_at = timezone.now()
		self.save(using=using)

	def force_delete(self, using=None, keep_parents=False):
		super(BaseModel, self).delete(using=using, keep_parents=keep_parents)

	class Meta:
		abstract = True
