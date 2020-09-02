from django import forms

job_type_list = ((1, "Permanent"), (2, "Temporary"),)


class NewJobForm(forms.Form):
  job_title = forms.CharField(
    label="Job Title",
    max_length=100,
    required=True,
  )

  job_description = forms.CharField(
    label="Description",
    max_length=80,
    required=True,
    widget=forms.Textarea(attrs={
      "class": "form-control",
      "placeholder": "Enter..",
    }),
  )

  job_skills = forms.CharField(
    label="Skills",
    required=False,
    widget=forms.Textarea(attrs={
      "class": "form-control",
      "placeholder": "Enter..",
    }),
  )

  job_type = forms.CharField(
    label="type",
    required=False,
    widget=forms.Select(choices=job_type_list)
  )

  job_city = forms.CharField(
    label="City",
    required=False,
  )

  salary = forms.IntegerField(
    label="Salary",
    required=False,
  )

  is_active = forms.BooleanField(
    label="Active",
    required=False
  )
