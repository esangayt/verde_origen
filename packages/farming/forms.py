from django import forms
from .models import Distribution

class DistributionInlineForm(forms.ModelForm):
    class Meta:
        model = Distribution
        fields = '__all__'

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        harvest = self.cleaned_data.get('harvest')
        if not harvest or quantity is None:
            return quantity
        # Exclude self from the queryset if editing
        if self.instance.pk:
            distributed = sum(d.quantity for d in harvest.distribution_set.exclude(pk=self.instance.pk))
        else:
            distributed = sum(d.quantity for d in harvest.distribution_set.all())
        remaining = harvest.quantity - distributed
        if quantity > remaining:
            raise forms.ValidationError(f"Cannot distribute more than remaining ({remaining} {harvest.measurement})")
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        type_ = cleaned_data.get('type')
        quality = cleaned_data.get('quality')
        if type_ == 'sale' and not quality:
            self.add_error('quality', 'Quality is required when type is Sale.')
        if type_ != 'sale' and quality:
            self.add_error('quality', 'Quality should only be set when type is Sale.')
        return cleaned_data
