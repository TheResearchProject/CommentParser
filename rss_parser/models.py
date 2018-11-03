# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Algorithm(models.Model):
    name = models.CharField(max_length=50, unique=True)
    positive_formula = models.CharField(max_length=30)
    neutral_formula = models.CharField(max_length=30)
    negative_formula = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'algorithm'    

class AlgorithmColor(models.Model):
    algorithm = models.ForeignKey("Algorithm")
    color = models.CharField(max_length=10)
    #Example: 
    # min_threshold = 0
    # max_threshold = 4
    # color will be on when: min_threshold <= value < max_threshold
    # be careful with max_threshold. If you want it to be, say, between 0 and 10
    # set it to min=0 and max=10.1, since the max value is non-inclusive to allow
    # many different ranges.
    min_threshold = models.FloatField()
    max_threshold = models.FloatField()
    
    class Meta:
        db_table = 'algorithm_color'
        unique_together = (('algorithm', 'color'),)
        
class Author(models.Model):
    name = models.CharField(max_length=255)
    long_name = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'author'    
        
class AuthorSummary(models.Model):
    author = models.ForeignKey('Author')
    avg_nr_words = models.FloatField(blank=True, null=True)
    avg_wordlen = models.FloatField(blank=True, null=True)
    avg_words_gt6 = models.FloatField(blank=True, null=True)
    avg_personal = models.FloatField(blank=True, null=True)
    avg_collective = models.FloatField(blank=True, null=True)
    indegree = models.FloatField(blank=True, null=True)
    indegree_centrality = models.FloatField(blank=True, null=True)
    outdegree = models.FloatField(blank=True, null=True)
    outdegree_centrality = models.FloatField(blank=True, null=True)
    degree = models.FloatField(blank=True, null=True)
    degree_centrality = models.FloatField(blank=True, null=True)
    avg_shared = models.FloatField(blank=True, null=True)
    pagerank = models.FloatField(blank=True, null=True)
    pagerank_weighted = models.FloatField(blank=True, null=True)
    nr_posts = models.IntegerField(blank=True, null=True)
    hub_score = models.FloatField(blank=True, null=True)
    authority_score = models.FloatField(blank=True, null=True)
    betweeness_centrality = models.FloatField(blank=True, null=True)
    closeness_centrality = models.FloatField(blank=True, null=True)
    clustering_coef = models.FloatField(blank=True, null=True)
    eccentricity = models.FloatField(blank=True, null=True)
    constraint = models.FloatField(blank=True, null=True)
    polarity_arousal = models.FloatField(blank=True, null=True)
    polarity_valence = models.FloatField(blank=True, null=True)
    
    class Meta:
        db_table = 'author_summary'        

class Cat1(models.Model):
    id = models.IntegerField(primary_key=True)
    label = models.CharField(max_length=50)
    description = models.TextField()

    class Meta:
        db_table = 'cat1'
        
class Category(models.Model):
    label = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    lower_label = models.CharField(max_length=50, blank=True, db_index=True)

    class Meta:
        db_table = 'category'        


class Comment(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    authorid = models.CharField(db_column='AuthorID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    author = models.ForeignKey('Author', null=True)
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    text = models.ForeignKey('Text', null=True)
    parent = models.ForeignKey('Comment',db_column='ParentID', blank=True, null=True)
    score = models.IntegerField(db_column='Score', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True, db_index=True)  # Field name made lowercase.
    authorshortname = models.CharField(db_column='AuthorShortname', max_length=50, blank=True, null=True)  # Field name made lowercase.
    newsitem = models.ForeignKey('Newsitem', db_column='NewsItemID', blank=True, null=True)  # Field name made lowercase.
    sentiment = models.FloatField(db_column='Sentiment', blank=True, null=True)  # Field name made lowercase.
    meanarousal = models.FloatField(db_column='meanArousal', blank=True, null=True)  # Field name made lowercase.
    stdvarousal = models.FloatField(db_column='stdvArousal', blank=True, null=True)  # Field name made lowercase.
    meanvalence = models.FloatField(db_column='meanValence', blank=True, null=True)  # Field name made lowercase.
    stdvvalence = models.FloatField(db_column='stdvValence', blank=True, null=True)  # Field name made lowercase.
    changed = models.IntegerField(blank=True, null=True)
    vmeansum = models.FloatField(db_column='vMeanSum', blank=True, null=True)  # Field name made lowercase.
    ameansum = models.FloatField(db_column='aMeanSum', blank=True, null=True)  # Field name made lowercase.
    dmeansum = models.FloatField(db_column='dMeanSum', blank=True, null=True)  # Field name made lowercase.
    vmeansum2 = models.FloatField(db_column='vMeanSum2', blank=True, null=True)  # Field name made lowercase.
    ameansum2 = models.FloatField(db_column='aMeanSum2', blank=True, null=True)  # Field name made lowercase.
    dmeansum2 = models.FloatField(db_column='dMeanSum2', blank=True, null=True)  # Field name made lowercase.
    vSDSum2 = models.FloatField(blank=True, null=True)
    aSDSum2 = models.FloatField(blank=True, null=True)
    dSDSum2 = models.FloatField(blank=True, null=True)    

    class Meta:
        db_table = 'comment'


class ExtraSettings(models.Model):
    setting_name = models.CharField(primary_key=True, max_length=100)
    setting_value = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'extra_settings'


class GeneralStats(models.Model):
    stat_name = models.CharField(primary_key=True, max_length=200)
    stat_value = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'general_stats'


class HotTopics(models.Model):
    topics = models.TextField(blank=True, null=True)
    algorithm = models.CharField(max_length=50, blank=True, null=True)
    period = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'hot_topics'


class Images(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    newsitemid = models.IntegerField(db_column='NewsItemId')  # Field name made lowercase.
    imagetype = models.CharField(db_column='ImageType', max_length=25)  # Field name made lowercase.
    image = models.TextField(db_column='Image')  # Field name made lowercase.
    imagesize = models.CharField(db_column='ImageSize', max_length=25)  # Field name made lowercase.
    imagecategory = models.CharField(db_column='ImageCategory', max_length=25, blank=True, null=True)  # Field name made lowercase.
    imagename = models.CharField(db_column='ImageName', max_length=255)  # Field name made lowercase.

    class Meta:
        db_table = 'images'

class Keyword(models.Model):
    algorithm = models.ForeignKey('Algorithm')
    text = models.ForeignKey('Text')
    keyword = models.CharField(max_length=2000)
    score = models.FloatField()

    class Meta:
        db_table = 'keyword'

class Labels(models.Model):
    id = models.IntegerField(primary_key=True)
    newsitem = models.IntegerField()
    tag = models.CharField(max_length=20)

    class Meta:
        db_table = 'labels'


class Newsitem(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.TextField(db_column='Title', blank=True, null=True)  # Field name made lowercase.
    lead = models.TextField(db_column='Lead', blank=True, null=True)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date', blank=True, null=True, db_index=True)  # Field name made lowercase.
    views = models.IntegerField(db_column='Views', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(db_column='Content', blank=True, null=True)  # Field name made lowercase.
    text = models.ForeignKey('Text', null=True)
    url = models.CharField(db_column='Url', max_length=200, blank=True, null=True)  # Field name made lowercase.
    author = models.ForeignKey('Author', null=True)
    idauthor = models.TextField(db_column='IdAuthor', blank=True, null=True)  # Field name made lowercase.
    score = models.IntegerField(blank=True, null=True)
    categories = models.ManyToManyField('Category',blank=True)
    cat1 = models.IntegerField(blank=True, null=True)
    twitter = models.IntegerField(db_column='Twitter', default=0)  # Field name made lowercase.
    facebook = models.IntegerField(db_column='Facebook', default=0)  # Field name made lowercase.
    googleplus = models.IntegerField(db_column='GooglePlus', default=0)  # Field name made lowercase.
    pinit = models.IntegerField(db_column='PinIt', default=0)  # Field name made lowercase.
    topics = models.ManyToManyField('Topic')

    class Meta:
        db_table = 'newsitem'

class Ratings(models.Model):
    f1 = models.SmallIntegerField(db_column='F1', primary_key=True)  # Field name made lowercase.
    word = models.CharField(db_column='Word', max_length=21, blank=True, null=True)  # Field name made lowercase.
    v_mean_sum = models.CharField(db_column='V.Mean.Sum', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_sd_sum = models.CharField(db_column='V.SD.Sum', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_rat_sum = models.SmallIntegerField(db_column='V.Rat.Sum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_mean_sum = models.CharField(db_column='A.Mean.Sum', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_sd_sum = models.CharField(db_column='A.SD.Sum', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_rat_sum = models.SmallIntegerField(db_column='A.Rat.Sum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_mean_sum = models.CharField(db_column='D.Mean.Sum', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_sd_sum = models.CharField(db_column='D.SD.Sum', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_rat_sum = models.SmallIntegerField(db_column='D.Rat.Sum', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_mean_m = models.CharField(db_column='V.Mean.M', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_sd_m = models.CharField(db_column='V.SD.M', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_rat_m = models.SmallIntegerField(db_column='V.Rat.M', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_mean_f = models.CharField(db_column='V.Mean.F', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_sd_f = models.CharField(db_column='V.SD.F', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_rat_f = models.SmallIntegerField(db_column='V.Rat.F', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_mean_m = models.CharField(db_column='A.Mean.M', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_sd_m = models.CharField(db_column='A.SD.M', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_rat_m = models.SmallIntegerField(db_column='A.Rat.M', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_mean_f = models.CharField(db_column='A.Mean.F', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_sd_f = models.CharField(db_column='A.SD.F', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_rat_f = models.SmallIntegerField(db_column='A.Rat.F', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_mean_m = models.CharField(db_column='D.Mean.M', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_sd_m = models.CharField(db_column='D.SD.M', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_rat_m = models.SmallIntegerField(db_column='D.Rat.M', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_mean_f = models.CharField(db_column='D.Mean.F', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_sd_f = models.CharField(db_column='D.SD.F', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_rat_f = models.SmallIntegerField(db_column='D.Rat.F', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_mean_y = models.CharField(db_column='V.Mean.Y', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_sd_y = models.CharField(db_column='V.SD.Y', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_rat_y = models.SmallIntegerField(db_column='V.Rat.Y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_mean_o = models.CharField(db_column='V.Mean.O', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_sd_o = models.CharField(db_column='V.SD.O', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_rat_o = models.SmallIntegerField(db_column='V.Rat.O', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_mean_y = models.CharField(db_column='A.Mean.Y', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_sd_y = models.CharField(db_column='A.SD.Y', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_rat_y = models.SmallIntegerField(db_column='A.Rat.Y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_mean_o = models.CharField(db_column='A.Mean.O', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_sd_o = models.CharField(db_column='A.SD.O', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_rat_o = models.SmallIntegerField(db_column='A.Rat.O', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_mean_y = models.CharField(db_column='D.Mean.Y', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_sd_y = models.CharField(db_column='D.SD.Y', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_rat_y = models.SmallIntegerField(db_column='D.Rat.Y', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_mean_o = models.CharField(db_column='D.Mean.O', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_sd_o = models.CharField(db_column='D.SD.O', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_rat_o = models.SmallIntegerField(db_column='D.Rat.O', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_mean_l = models.CharField(db_column='V.Mean.L', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_sd_l = models.CharField(db_column='V.SD.L', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_rat_l = models.SmallIntegerField(db_column='V.Rat.L', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_mean_h = models.CharField(db_column='V.Mean.H', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_sd_h = models.CharField(db_column='V.SD.H', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    v_rat_h = models.SmallIntegerField(db_column='V.Rat.H', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_mean_l = models.CharField(db_column='A.Mean.L', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_sd_l = models.CharField(db_column='A.SD.L', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_rat_l = models.SmallIntegerField(db_column='A.Rat.L', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_mean_h = models.CharField(db_column='A.Mean.H', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_sd_h = models.CharField(db_column='A.SD.H', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    a_rat_h = models.SmallIntegerField(db_column='A.Rat.H', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_mean_l = models.CharField(db_column='D.Mean.L', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_sd_l = models.CharField(db_column='D.SD.L', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_rat_l = models.SmallIntegerField(db_column='D.Rat.L', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_mean_h = models.CharField(db_column='D.Mean.H', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_sd_h = models.CharField(db_column='D.SD.H', max_length=4, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    d_rat_h = models.SmallIntegerField(db_column='D.Rat.H', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        db_table = 'ratings'
        
class Result(models.Model):
    algorithm = models.ForeignKey('Algorithm')
    text = models.ForeignKey('Text', null=True)
    sequence = models.IntegerField(null=True)
    value = models.TextField()
    date = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'result'    
    

class Text(models.Model):
    text = models.TextField()
    summary = models.TextField(null=True)
    wordcount = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'text'    
        
class Topic(models.Model):
    name = models.CharField(max_length=100)

class Word(models.Model):
    texts = models.ManyToManyField('Text', blank=True)
    noun  = models.CharField(max_length=1000, blank=True)
    word  = models.CharField(max_length=1000)
    tag   = models.CharField(max_length=20)
    
    class Meta:
        db_table = 'word'    
    
#PHP website models

class Permission(models.Model):
    name = models.CharField(primary_key=True, max_length=25)
    description = models.CharField(max_length=64)
    category = models.CharField(max_length=25)

    class Meta:
        db_table = 'Permission'


class Role(models.Model):
    name = models.CharField(primary_key=True, max_length=35)
    description = models.CharField(max_length=64)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    createdbyid = models.IntegerField(db_column='createdById')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt', blank=True, null=True)  # Field name made lowercase.
    updatedbyid = models.IntegerField(db_column='updatedById', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Role'


class Rolepermission(models.Model):
    rolename = models.CharField(db_column='roleName', max_length=35)  # Field name made lowercase.
    permissionname = models.CharField(db_column='permissionName', max_length=35)  # Field name made lowercase.

    class Meta:
        db_table = 'RolePermission'
        unique_together = (('rolename', 'permissionname'),)


class User(models.Model):
    firstname = models.CharField(db_column='firstName', max_length=35)  # Field name made lowercase.
    lastname = models.CharField(db_column='lastName', max_length=35)  # Field name made lowercase.
    email = models.CharField(max_length=64)
    username = models.CharField(max_length=35)
    password = models.CharField(max_length=64)
    oldpassword = models.CharField(db_column='oldPassword', max_length=64)  # Field name made lowercase.
    role = models.CharField(max_length=25)
    createdat = models.DateTimeField(db_column='createdAt')  # Field name made lowercase.
    createdbyid = models.IntegerField(db_column='createdById')  # Field name made lowercase.
    updatedat = models.DateTimeField(db_column='updatedAt')  # Field name made lowercase.
    updatedbyid = models.IntegerField(db_column='updatedById')  # Field name made lowercase.
    timezone = models.CharField(db_column='timeZone', max_length=35, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField()
    type = models.IntegerField()

    class Meta:
        db_table = 'User'
