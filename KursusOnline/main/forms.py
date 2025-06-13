from django import forms
from .models import Member
from .models import MateriKursus


class AdminLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300',
        'placeholder': 'Password'
    }))
class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300',
        'placeholder': 'Email'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full px-4 py-2 border rounded-lg focus:outline-none focus:ring focus:border-blue-300',
        'placeholder': 'Password'
    }))
class MateriForm(forms.ModelForm):
    class Meta:
        model = MateriKursus
        fields = ['judul', 'deskripsi', 'file_url', 'tipe_materi', 'urutan']
        widgets = {
            'judul': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-md bg-gray-100 text-gray-900 focus:ring focus:ring-blue-400',
                'placeholder': 'Masukkan judul materi'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-md bg-gray-100 text-gray-900 focus:ring focus:ring-blue-400',
                'placeholder': 'Masukkan deskripsi...',
                'rows': 4
            }),
            'file_url': forms.ClearableFileInput(attrs={
                'class': 'w-full bg-gray-100 text-gray-900 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer'
            }),
            'tipe_materi': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-md bg-gray-100 text-gray-900 focus:ring focus:ring-blue-400'
            }),
            'urutan': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-md bg-gray-100 text-gray-900 focus:ring focus:ring-blue-400'
            }),
        }
