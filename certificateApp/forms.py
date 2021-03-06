from django.conf import settings
from .models import UserProfile
from django import forms
from .models import Report, PersonalDetail, Project


class ReportSubmissionForm(forms.ModelForm):
    class Meta():
        model = Report
        fields = ['project_name', 'upload_report']


class PersonalDetailForm(forms.ModelForm):
    class Meta:
        model = PersonalDetail
        fields = ['ph_contact_no', 'whatsapp_no', 'project', 'profile',
                  'type_of_internship',
                  'pan_number', 'aadhaar', 'emergency_contact_no',
                  'bank_account_no', 'ifsc_code', 'dob', 'permanent_address',
                  'current_address', 'biometric_id_number', 'internship_tenure', 'resume'
                  ]
        widgets = {
            'ph_contact_no': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'pattern': '[0-9]{10}',
            }),

            'whatsapp_no': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'pattern': '[0-9]{10}',
            }),

            'emergency_contact_no': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'pattern': '[0-9]{10}',
            }),

            'project': forms.Select(attrs={
                'class': 'form-select'
            }),

            'profile': forms.Select(attrs={
                'class': 'form-select'
            }),

            'type_of_internship': forms.Select(attrs={
                'class': 'form-select'
            }),

            'internship_tenure': forms.Select(attrs={
                'class': 'form-select'
            }),

            'pan_number': forms.TextInput(attrs={
                'class': 'form-control',
                'minlength': '10',
            }),

            'aadhaar': forms.TextInput(attrs={
                'class': 'form-control',
                'minlength': '10',
            }),

            'bank_account_no': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]+'
            }),

            'ifsc_code': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'biometric_id_number': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'current_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'minlength': '20'
            }),

            'permanent_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'minlength': '20'
            }),

            'dob': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
        }

        def clean(self):
            cleaned_data = super().clean()

            contact = cleaned_data.get("ph_contact_no")
            if not contact.isnumeric() and len(contact) != 10:
                msg = "invalid Phone contact number."
                self.add_error('ph_contact_no', msg)

            whatsapp = cleaned_data.get("whatsapp_no")
            if not whatsapp.isnumeric() and len(whatsapp) != 10:
                msg = "invalid Whatsapp number."
                self.add_error('whatsapp_no', msg)


class ProjectDetailsForm(forms.ModelForm):
    class Meta():
        model = Project
        # fields = ['profile','project_worked_on',
        #     'status','tenure','joining_date',
        #     'end_date','upload_traker_link',
        #     'detail_of_work','mentor_or_leader'
        # ]
        fields = ['profile', 'project_worked_on',
                  'status', 'tenure', 'joining_date',
                  'end_date', 'upload_traker_link',
                  'detail_of_work', 'mentor_or_leader'
                  ]
        widgets = {
            'profile': forms.Select(attrs={
                'class': 'form-select',
                'readonly': 'readonly'
            }),

            'project_worked_on': forms.Select(attrs={
                'class': 'form-select',
                'readonly': 'readonly'
            }),

            'status': forms.Select(attrs={
                'class': 'form-select'
            }),

            'tenure': forms.Select(attrs={
                'class': 'form-select',
                'readonly': 'readonly'
            }),

            'joining_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'readonly': 'readonly'
            }),

            'end_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'readonly': 'readonly'
            }),

            'upload_traker_link': forms.URLInput({
                'class': 'form-control'
            }),

            'detail_of_work': forms.Textarea(attrs={
                'class': 'form-control',
                'minlength': '30',
                'rows': '3'
            }),

            'mentor_or_leader': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3'
            })
        }


# -------------------------------------------------------------------------------------


class InternForm(forms.ModelForm):
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
    password.widget.attrs.update({'class': 'form-control'})
    confirm_password = forms.CharField(
        max_length=255, widget=forms.PasswordInput)
    email = forms.EmailField(widget=forms.EmailInput)
    email.widget.attrs.update({'class': 'form-control'})
    confirm_password.widget.attrs.update({'class': 'form-control'})

    class Meta():
        model = UserProfile
        fields = ('first_name', 'last_name', 'email',
                  'password', 'confirm_password')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            'password': forms.PasswordInput(attrs={
                'class': 'form-control'
            })
        }

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')

        if len(last_name) < 3:
            raise forms.ValidationError('Size less than 3')

        return last_name

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')

        if len(first_name) < 3:
            raise forms.ValidationError('Size less than 3')

        return first_name

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                f'Password does not match{confirm_password} {password}')
        if len(password) < 8:
            raise forms.ValidationError('Weak Password')
        return password
