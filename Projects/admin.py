from django.contrib import admin

from Projects.models import  *

admin.site.register(Beneficiary)
admin.site.register(Goals)
admin.site.register(Goods_Given_From_Member_To_Project)
admin.site.register(Goods_Required_For_Project)
admin.site.register(Influence)

admin.site.register(Member_Skills)
admin.site.register(Offer_Time)
admin.site.register(Post)
admin.site.register(Project)
admin.site.register(Project_Member_Relationship)

admin.site.register(Transact)
admin.site.register(Task)
