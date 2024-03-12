# Generated by Django 3.2.25 on 2024-03-11 10:45

import cms.models.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('djangocms_moderation', '0001_initial'), ('djangocms_moderation', '0002_auto_20180905_1152'), ('djangocms_moderation', '0003_auto_20180903_1206'), ('djangocms_moderation', '0004_auto_20180907_1206'), ('djangocms_moderation', '0005_auto_20180919_1348'), ('djangocms_moderation', '0006_auto_20181001_1840'), ('djangocms_moderation', '0007_auto_20181002_1725'), ('djangocms_moderation', '0008_auto_20181002_1833'), ('djangocms_moderation', '0009_auto_20181005_1534'), ('djangocms_moderation', '0010_auto_20181008_1317'), ('djangocms_moderation', '0011_auto_20181008_1328'), ('djangocms_moderation', '0012_auto_20181016_1319'), ('djangocms_moderation', '0013_auto_20181122_1110'), ('djangocms_moderation', '0014_auto_20190313_1638'), ('djangocms_moderation', '0014_auto_20190315_1723'), ('djangocms_moderation', '0016_moderationrequesttreenode'), ('djangocms_moderation', '0017_auto_20220831_0727')]

    initial = True

    dependencies = [
        ('cms', '0028_remove_page_placeholders'),
        ('djangocms_versioning', '0010_version_proxies'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('cms', '0020_old_tree_cleanup'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfirmationPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
                ('content_type', models.CharField(choices=[('plain', 'Plain'), ('form', 'Form')], default='form', max_length=50, verbose_name='Content Type')),
                ('template', models.CharField(choices=[('djangocms_moderation/moderation_confirmation.html', 'Default')], default='djangocms_moderation/moderation_confirmation.html', max_length=100, verbose_name='Template')),
                ('content', cms.models.fields.PlaceholderField(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, slotname='confirmation_content', to='cms.placeholder')),
            ],
            options={
                'verbose_name': 'Confirmation Page',
                'verbose_name_plural': 'Confirmation Pages',
            },
        ),
        migrations.CreateModel(
            name='ModerationCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='collection name')),
                ('status', models.CharField(choices=[('COLLECTING', 'Collecting'), ('IN_REVIEW', 'In Review'), ('ARCHIVED', 'Archived'), ('CANCELLED', 'Cancelled')], db_index=True, default='COLLECTING', max_length=10)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
        ),
        migrations.CreateModel(
            name='ModerationRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('de', 'German')], max_length=20, verbose_name='language')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='is active')),
                ('date_sent', models.DateTimeField(auto_now_add=True, verbose_name='date sent')),
                ('compliance_number', models.CharField(blank=True, editable=False, max_length=32, null=True, unique=True, verbose_name='compliance number')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderation_requests', to='djangocms_moderation.moderationcollection')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangocms_versioning.version', verbose_name='version')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='author')),
            ],
            options={
                'verbose_name': 'Request',
                'verbose_name_plural': 'Requests',
                'ordering': ['id'],
                'unique_together': {('collection', 'version')},
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='name')),
                ('confirmation_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='djangocms_moderation.confirmationpage', verbose_name='confirmation page')),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='auth.group', verbose_name='group')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, unique=True, verbose_name='name')),
                ('is_default', models.BooleanField(default=False, verbose_name='is default')),
                ('identifier', models.CharField(blank=True, default='', help_text="Identifier is a 'free' field you could use for internal purposes. For example, it could be used as a workflow specific prefix of a compliance number", max_length=128, verbose_name='identifier')),
                ('requires_compliance_number', models.BooleanField(default=False, help_text='Does the Compliance number need to be generated before the moderation request is approved? Please select the compliance number backend below', verbose_name='requires compliance number?')),
                ('compliance_number_backend', models.CharField(choices=[('djangocms_moderation.backends.uuid4_backend', 'Unique alpha-numeric string'), ('djangocms_moderation.backends.sequential_number_backend', 'Sequential number'), ('djangocms_moderation.backends.sequential_number_with_identifier_prefix_backend', 'Sequential number with identifier prefix')], default='djangocms_moderation.backends.uuid4_backend', max_length=255, verbose_name='compliance number backend')),
            ],
            options={
                'verbose_name': 'Workflow',
                'verbose_name_plural': 'Workflows',
            },
        ),
        migrations.CreateModel(
            name='WorkflowStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_required', models.BooleanField(default=True, verbose_name='is mandatory')),
                ('order', models.PositiveIntegerField()),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangocms_moderation.role', verbose_name='role')),
                ('workflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='djangocms_moderation.workflow', verbose_name='workflow')),
            ],
            options={
                'verbose_name': 'Step',
                'verbose_name_plural': 'Steps',
                'ordering': ('order',),
                'unique_together': {('role', 'workflow')},
            },
        ),
        migrations.AddField(
            model_name='moderationcollection',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderation_collections', to='djangocms_moderation.workflow', verbose_name='workflow'),
        ),
        migrations.CreateModel(
            name='RequestComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, verbose_name='message')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('moderation_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangocms_moderation.moderationrequest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='moderationcollection',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='owner'),
        ),
        migrations.AlterModelOptions(
            name='moderationcollection',
            options={'permissions': (('can_change_author', 'Can change collection author'),), 'verbose_name': 'collection'},
        ),
        migrations.CreateModel(
            name='CollectionComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True, verbose_name='message')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='author')),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangocms_moderation.moderationcollection')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ConfirmationFormSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(blank=True, editable=False)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='by user')),
                ('confirmation_page', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='+', to='djangocms_moderation.confirmationpage', verbose_name='confirmation page')),
                ('for_step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='djangocms_moderation.workflowstep', verbose_name='for step')),
                ('moderation_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='form_submissions', to='djangocms_moderation.moderationrequest', verbose_name='moderation request')),
            ],
            options={
                'verbose_name': 'Confirmation Form Submission',
                'verbose_name_plural': 'Confirmation Form Submissions',
                'unique_together': {('moderation_request', 'for_step')},
            },
        ),
        migrations.CreateModel(
            name='ModerationRequestAction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('resubmitted', 'Resubmitted'), ('start', 'Started'), ('rejected', 'Rejected'), ('approved', 'Approved'), ('cancelled', 'Cancelled'), ('finished', 'Finished')], max_length=30, verbose_name='status')),
                ('message', models.TextField(blank=True, verbose_name='message')),
                ('date_taken', models.DateTimeField(auto_now_add=True, verbose_name='date taken')),
                ('is_archived', models.BooleanField(default=False)),
                ('by_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL, verbose_name='by user')),
                ('step_approved', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='djangocms_moderation.workflowstep', verbose_name='step approved')),
                ('to_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='djangocms_moderation.role', verbose_name='to role')),
                ('to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='to user')),
                ('moderation_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions', to='djangocms_moderation.moderationrequest', verbose_name='moderation_request')),
            ],
            options={
                'verbose_name': 'Action',
                'verbose_name_plural': 'Actions',
                'ordering': ('date_taken',),
            },
        ),
        migrations.AlterField(
            model_name='moderationcollection',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='moderator'),
        ),
        migrations.AlterModelOptions(
            name='moderationcollection',
            options={'permissions': (('can_change_author', 'Can change collection author'), ('cancel_moderationcollection', 'Can cancel collection')), 'verbose_name': 'collection'},
        ),
        migrations.CreateModel(
            name='ModerationRequestTreeNode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('moderation_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='djangocms_moderation.moderationrequest', verbose_name='moderation_request')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]
