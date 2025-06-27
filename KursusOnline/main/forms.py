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
                'class': 'w-full px-4 py-2 rounded-md bg-gray-700 text-white focus:ring focus:ring-blue-400',
                'placeholder': 'Masukkan judul materi'
            }),
            'deskripsi': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 rounded-md bg-gray-700 text-white focus:ring focus:ring-blue-400',
                'placeholder': 'Masukkan deskripsi...',
                'rows': 4
            }),
            'file_url': forms.ClearableFileInput(attrs={
                'class': 'w-full text-white bg-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:bg-blue-600 file:text-white hover:file:bg-blue-700 cursor-pointer'
            }),
            'tipe_materi': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-md bg-gray-700 text-white focus:ring focus:ring-blue-400'
            }),
            'urutan': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 rounded-md bg-gray-700 text-white focus:ring focus:ring-blue-400'
            }),
        }


    def __init__(self, *args, **kwargs):
        self.kursus = kwargs.pop('kursus', None)
        self.instance_id = kwargs.get('instance').id if 'instance' in kwargs and kwargs.get('instance') else None
        super().__init__(*args, **kwargs)

    def clean_urutan(self):
        urutan = self.cleaned_data['urutan']
        if self.kursus:
            # Cek apakah sudah ada materi lain dengan urutan ini
            qs = MateriKursus.objects.filter(kursus=self.kursus, urutan=urutan)
            if self.instance_id:
                qs = qs.exclude(pk=self.instance_id)  # Jika sedang edit, abaikan data sendiri
            if qs.exists():
                raise forms.ValidationError("Sudah ada materi lain dengan urutan ini.")
        return urutan

class DummyMateriForm(forms.Form):
    judul = forms.CharField(
        label='Judul',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 rounded bg-gray-700 text-white border border-gray-600'
        })
    )
    deskripsi = forms.CharField(
        label='Deskripsi',
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 rounded bg-gray-700 text-white border border-gray-600'
        })
    )
    tipe_materi = forms.ChoiceField(
        label='Tipe Materi',
        choices=[('modul', 'Modul'), ('video', 'Video')],
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 rounded bg-gray-700 text-white border border-gray-600'
        })
    )
    urutan = forms.IntegerField(
        label='Urutan',
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 rounded bg-gray-700 text-white border border-gray-600'
        })
    )
    file_url = forms.FileField(
        label='File Materi',
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full px-3 py-2 rounded bg-gray-700 text-white border border-gray-600'
        })
    )