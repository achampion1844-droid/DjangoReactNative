from rest_framework import serializers
from .models import Article, Subject, Subject_Info_Type, Assignment, PhotoTest, Chat, ChatMembership, Message
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from django.conf import settings
from django.contrib.auth import get_user_model

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'created_at', 'subject_ID', 'user']
        read_only_fields = ['user']


class AssignmentSerializer(serializers.ModelSerializer):
    # use multiple=True only if it is a many to many relationship
    subject = SubjectSerializer(read_only=True)
    subject_id = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), #primary key related fields looks up the uuid primary key in all the subject objects, validates it exists and returns the subject objects with that primary key
        source='subject', #saves the subject object just gotten to the subject field in the assignment model
        write_only=True #means only post or put requests need this field
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    # extra_dates = serializers.SerializerMethodField()




    class Meta:
        model = Assignment
        fields = [
            'user', 
            'assignment_ID', 
            'assignment_description', 
            'assignment_name','date_added', 
            'date_started', 
            'remaining_study_sessions', 
            'subject',
            'subject_id', 
            'icon', 
            'is_Completed',
            # 'extra_dates',
            'intervals',
        ]

    def validate_intervals(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("Intervals must be an object.")
        for key, val in value.items():
            if not str(key).isdigit():
                raise serializers.ValidationError(
                    f"Interval key '{key}' must be a whole number of days."
                )
            if not isinstance(val, list) or not val:
                raise serializers.ValidationError(
                    f"Interval '{key}' must be a non-empty list."
                )
        return value

    # def get_extra_dates(self, obj):
    #     result = {}
    #     for d, value in obj.intervals.items():
    #         try:
    #             days = int(d)
    #         except (TypeError, ValueError):
    #             continue
    #         result[f"{days}_days"] = [obj.date_for(days), value[0]]
    #     return result


class Subject_Info_TypeSerializer(serializers.ModelSerializer):
    subject_name = SubjectSerializer(read_only=True)
    subject_details = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), source='subject_name')
    
    class Meta:
        model = Subject_Info_Type
        fields = [
            'icon',
            'subject_name',
            'num_sub_study_items',
            'id',
            'subject_details',
        ]


class PhotoTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoTest
        fields = [
            'name',
            'image',
        ]





### 4. When and How to Use `select_related` vs. `prefetch_related`
# Both tools prevent the **N+1 Query Problem** (where looping through 50 items triggers 50 separate database lookups). You choose between them based on **how many objects** are on the other side of the relationship.

# | Feature | `select_related` | `prefetch_related` |
# | :--- | :--- | :--- |y
# | **Relationship Type** | **Single** object (`ForeignKey`, `OneToOneField`) | **Multiple** objects (`ManyToManyField`, reverse `ForeignKey`) |
# | **How it works** | Uses a single SQL `INNER JOIN` to merge tables into one big query. | Runs 2 separate SQL queries and connects them together in Python. |
# | **Direction** | "Looking up" to a parent (e.g., a Message belongs to **one** Creator). | "Looking down" to children (e.g., a Chat has **many** Members). |





class ChatSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Chat
        fields = ['chat_id', 'is_dm', 'name', 'created_at', 'members']
        read_only_fields = ['chat_id', 'created_at']

    def validate(self, attrs): #what is attrs and self?
        if self.instance is None:  # creating a brand new chat if the instance does not exist
            is_dm = attrs.get("is_dm", True) # in the is_dm, tries to get the true false value of is_dm or else it returns true if no value was provided
            name = attrs.get("name", "").strip()
            if not is_dm and not name:
                raise serializers.ValidationError({"name": "Group chats must have a name."})
            attrs["name"] = name
        else:  # updating
            if self.instance.is_dm and "name" in attrs: #what is "name" in this line and how do i create var like it?
                raise serializers.ValidationError("Direct messages cannot be renamed.")
            if not self.instance.is_dm:
                name = attrs.get("name", self.instance.name).strip()
                if not name:
                    raise serializers.ValidationError({"name": "Group chats must have a name."})
                attrs["name"] = name
        return attrs


class ChatMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    chat_id = serializers.UUIDField(source="chat.chat_id", read_only=True) #can all serializers pull across model fields?
    class Meta:
        model = ChatMembership
        fields = ['user', 'chat_id', 'last_read_at']
        read_only_fields = ['user', 'chat_id']


class AddMemberSerializer(serializers.ModelSerializer):
    chat = serializers.SlugRelatedField(slug_field='chat_id', queryset=Chat.objects.all(),) #how do slug fields work?
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = ChatMembership
        fields = ['chat', 'user']

    def validate(self, attrs): #attrs is a dictionary containing all the values that you set in the model assumeing null isn't true
        request_user = self.context["request"].user #what is self.context?
        chat = attrs["chat"]
        new_user = attrs["user"]
        if chat.is_dm:
            raise serializers.ValidationError("Cannot add members to a direct message.")
        if not chat.memberships.filter(user=request_user).exists():
            raise PermissionDenied("You are not a member of this chat.")
        if chat.memberships.filter(user=new_user).exists():
            raise serializers.ValidationError({"user": "This user is already a member."})
        return attrs


class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.SlugRelatedField(slug_field="chat_id", queryset=Chat.objects.all(),)
    creator = serializers.ReadOnlyField(source="creator.id")
    class Meta:
        model = Message
        fields= ['message_id', 'chat', 'creator', 'text', 'created_at']
        read_only_fields = ["message_id", "creator", "created_at"]

    def validate_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message text cannot be blank.")
        return value





# class MessageLifecycleSerializer(serializers.ModelSerializer):
#     chat = serializers.SlugRelatedField(slug_field="chat_id", queryset=Chat.objects.all())
#     creator = serializers.ReadOnlyField(source="creator.username")

#     class Meta:
#         model = Message
#         fields = ["message_id", "chat", "creator", "text", "created_at"]
#         read_only_fields = ["message_id", "creator", "created_at"]

#     # 1. Runs when the serializer is initialized (before validation)
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # ACCESS: self.context (if passed by the view)
#         # ACCESS (also): args, kwargs (raw constructor arguments: data=, instance=, many=, partial=)
#         # ACCESS (also): self.fields (all declared fields), self.partial (True on PATCH)
#         request = self.context.get("request")
#         if request and not request.user.is_staff:
#             # Example: dynamically lock a field for non-admin users
#             self.fields["chat"].read_only = False

#     # 2. Runs first on incoming raw JSON before type checking
#     def to_internal_value(self, data):
#         # ACCESS: 'data' is the raw dictionary from request.data
#         # ACCESS (also): self.context["request"], self.context["view"], self.initial_data
#         # Example: clean up raw input before DRF parses it
#         if "text" in data and isinstance(data["text"], str):
#             data = data.copy()  # request.data is immutable, so copy first
#             data["text"] = data["text"].strip()
#         return super().to_internal_value(data)

#     # 3. Runs on ONE specific field after basic type conversion
#     def validate_text(self, value):
#         # ACCESS: 'value' is the single Python value for 'text'
#         # ACCESS (also): self.context["request"].user, self.instance (None on POST)
#         if len(value) < 1:
#             raise serializers.ValidationError("Message cannot be empty.")
#         return value

#     # 4. Runs across ALL fields together after individual field checks pass
#     def validate(self, attrs):
#         # ACCESS:
#         # - attrs: dict of all validated incoming fields (e.g., attrs["chat"], attrs["text"])
#         # - self.instance: existing DB object (on PATCH/PUT) or None (on POST)
#         # - self.context["request"].user: the logged-in user
#         # ACCESS (also): attrs["chat"] (resolved Chat object), attrs.get("text"),
#         #   self.instance.chat, self.instance.text, self.instance.creator_id (on PATCH/PUT)
#         user = self.context["request"].user
#         chat = attrs.get("chat") or self.instance.chat

#         if not chat.memberships.filter(user=user).exists():
#             raise serializers.ValidationError("You must be a member of this chat.")
#         return attrs

#     # 5A. Runs ONLY on POST when view calls serializer.save()
#     def create(self, validated_data):
#         # ACCESS: 'validated_data' (everything from attrs + extra kwargs passed to .save())
#         # Note: if the view called serializer.save(creator=user), 'creator' is inside validated_data!
#         # ACCESS (also): validated_data["chat"] (Chat object), validated_data["text"],
#         #   validated_data["creator"] (if injected by the view), self.context["request"].user
#         return Message.objects.create(**validated_data)

#     # 5B. Runs ONLY on PATCH/PUT when view calls serializer.save()
#     def update(self, instance, validated_data):
#         # ACCESS:
#         # - instance: the existing Message row in the DB
#         # - validated_data: only the fields the user sent to update
#         # ACCESS (also): instance.message_id, instance.id, instance.creator_id,
#         #   instance.chat, instance.created_at, instance.text (old value before the change)
#         instance.text = validated_data.get("text", instance.text)
#         instance.save()
#         return instance

#     # 6. Runs on the way OUT when converting a Python object into JSON
#     def to_representation(self, instance):
#         # ACCESS: 'instance' is the Message object being sent back to the frontend
#         # ACCESS (also): instance.message_id, instance.creator.username (via "creator" field),
#         #   instance.chat.chat_id (via "chat" field), instance.created_at, instance.text
#         representation = super().to_representation(instance)
#         # ACCESS (also): representation (the dict of fields built so far)
#         # Example: add a computed field to the outgoing JSON
#         representation["character_count"] = len(instance.text)
#         return representation


