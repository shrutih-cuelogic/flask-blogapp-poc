from flask_wtf import FlaskForm
from wtforms import (
StringField, 
TextAreaField, 
DateField,
SubmitField,
HiddenField,
validators
)

# Comment form class
class UserCommentForm(FlaskForm):
	"""
	CommentForm for registered users to comment any blog
	"""
	content = TextAreaField('Content',[validators.DataRequired(), validators.length(max=200)])
	parent_comment_id = HiddenField("",[validators.optional()])
	submit = SubmitField('Comment')
	comment_created_on = DateField('Commented on',[
		validators.optional()],
		format='%Y/%m/%d')
