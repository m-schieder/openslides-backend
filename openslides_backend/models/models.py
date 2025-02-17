# Code generated. DO NOT EDIT.

from openslides_backend.models import fields
from openslides_backend.models.base import Model
from openslides_backend.shared.patterns import Collection

MODELS_YML_CHECKSUM = "3fd01ad6a70c3946ff894b9d319c02a8"


class Organization(Model):
    collection = Collection("organization")
    verbose_name = "organization"

    id = fields.IntegerField()
    name = fields.CharField()
    description = fields.HTMLStrictField()
    legal_notice = fields.TextField()
    privacy_policy = fields.TextField()
    login_text = fields.TextField()
    reset_password_verbose_errors = fields.BooleanField()
    enable_electronic_voting = fields.BooleanField()
    enable_chat = fields.BooleanField()
    limit_of_meetings = fields.IntegerField(
        default=0,
        constraints={
            "description": "Maximum of active meetings for the whole organization. 0 means no limitation at all",
            "minimum": 0,
        },
    )
    limit_of_users = fields.IntegerField(
        default=0,
        constraints={
            "description": "Maximum of active users for the whole organization. 0 means no limitation at all",
            "minimum": 0,
        },
    )
    committee_ids = fields.RelationListField(
        to={Collection("committee"): "organization_id"}
    )
    active_meeting_ids = fields.RelationListField(
        to={Collection("meeting"): "is_active_in_organization_id"}
    )
    archived_meeting_ids = fields.RelationListField(
        to={Collection("meeting"): "is_archived_in_organization_id"}
    )
    template_meeting_ids = fields.RelationListField(
        to={Collection("meeting"): "template_for_organization_id"}
    )
    organization_tag_ids = fields.RelationListField(
        to={Collection("organization_tag"): "organization_id"}
    )
    theme_id = fields.RelationField(
        to={Collection("theme"): "theme_for_organization_id"}, required=True
    )
    theme_ids = fields.RelationListField(to={Collection("theme"): "organization_id"})
    mediafile_ids = fields.RelationListField(
        to={Collection("mediafile"): "owner_id"}, on_delete=fields.OnDelete.CASCADE
    )
    users_email_sender = fields.CharField(default="OpenSlides")
    users_email_replyto = fields.CharField()
    users_email_subject = fields.CharField(default="OpenSlides access data")
    users_email_body = fields.TextField(
        default="Dear {name},\n\nthis is your personal OpenSlides login:\n\n{url}\nUsername: {username}\nPassword: {password}\n\n\nThis email was generated automatically."
    )
    url = fields.CharField(default="https://example.com")


class User(Model):
    collection = Collection("user")
    verbose_name = "user"

    id = fields.IntegerField()
    username = fields.CharField(required=True)
    pronoun = fields.CharField()
    title = fields.CharField()
    first_name = fields.CharField()
    last_name = fields.CharField()
    is_active = fields.BooleanField()
    is_physical_person = fields.BooleanField(default=True)
    password = fields.CharField()
    default_password = fields.CharField()
    can_change_own_password = fields.BooleanField(default=True)
    gender = fields.CharField(constraints={"enum": ["male", "female", "diverse"]})
    email = fields.CharField()
    default_number = fields.CharField()
    default_structure_level = fields.CharField()
    default_vote_weight = fields.DecimalField(
        default="1.000000", constraints={"minimum": 0}
    )
    last_email_send = fields.TimestampField()
    is_demo_user = fields.BooleanField()
    organization_management_level = fields.CharField(
        constraints={
            "description": "Hierarchical permission level for the whole organization.",
            "enum": ["superadmin", "can_manage_organization", "can_manage_users"],
        }
    )
    is_present_in_meeting_ids = fields.RelationListField(
        to={Collection("meeting"): "present_user_ids"}
    )
    committee_ids = fields.RelationListField(
        to={Collection("committee"): "user_ids"},
        read_only=True,
        constraints={"description": "Calculated field."},
    )
    committee__management_level = fields.TemplateRelationListField(
        index=10,
        to={Collection("committee"): "user_$_management_level"},
        replacement_enum=["can_manage"],
    )
    forwarding_committee_ids = fields.RelationListField(
        to={Collection("committee"): "forwarding_user_id"}
    )
    comment_ = fields.TemplateHTMLStrictField(
        index=8,
        replacement_collection=Collection("meeting"),
    )
    number_ = fields.TemplateCharField(
        index=7,
        replacement_collection=Collection("meeting"),
    )
    structure_level_ = fields.TemplateCharField(
        index=16,
        replacement_collection=Collection("meeting"),
    )
    about_me_ = fields.TemplateHTMLStrictField(
        index=9,
        replacement_collection=Collection("meeting"),
    )
    vote_weight_ = fields.TemplateDecimalField(
        index=12,
        replacement_collection=Collection("meeting"),
        constraints={"minimum": 0},
    )
    group__ids = fields.TemplateRelationListField(
        index=6,
        replacement_collection=Collection("meeting"),
        to={Collection("group"): "user_ids"},
    )
    speaker__ids = fields.TemplateRelationListField(
        index=8,
        replacement_collection=Collection("meeting"),
        to={Collection("speaker"): "user_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    personal_note__ids = fields.TemplateRelationListField(
        index=14,
        replacement_collection=Collection("meeting"),
        to={Collection("personal_note"): "user_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    supported_motion__ids = fields.TemplateRelationListField(
        index=17,
        replacement_collection=Collection("meeting"),
        to={Collection("motion"): "supporter_ids"},
    )
    submitted_motion__ids = fields.TemplateRelationListField(
        index=17,
        replacement_collection=Collection("meeting"),
        to={Collection("motion_submitter"): "user_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    poll_voted__ids = fields.TemplateRelationListField(
        index=11,
        replacement_collection=Collection("meeting"),
        to={Collection("poll"): "voted_ids"},
    )
    option__ids = fields.TemplateRelationListField(
        index=7,
        replacement_collection=Collection("meeting"),
        to={Collection("option"): "content_object_id"},
    )
    vote__ids = fields.TemplateRelationListField(
        index=5,
        replacement_collection=Collection("meeting"),
        to={Collection("vote"): "user_id"},
    )
    vote_delegated_vote__ids = fields.TemplateRelationListField(
        index=20,
        replacement_collection=Collection("meeting"),
        to={Collection("vote"): "delegated_user_id"},
    )
    assignment_candidate__ids = fields.TemplateRelationListField(
        index=21,
        replacement_collection=Collection("meeting"),
        to={Collection("assignment_candidate"): "user_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    projection__ids = fields.TemplateRelationListField(
        index=11,
        replacement_collection=Collection("meeting"),
        to={Collection("projection"): "content_object_id"},
    )
    vote_delegated__to_id = fields.TemplateRelationField(
        index=15,
        replacement_collection=Collection("meeting"),
        to={Collection("user"): "vote_delegations_$_from_ids"},
    )
    vote_delegations__from_ids = fields.TemplateRelationListField(
        index=17,
        replacement_collection=Collection("meeting"),
        to={Collection("user"): "vote_delegated_$_to_id"},
    )
    chat_message__ids = fields.TemplateRelationListField(
        index=13,
        replacement_collection=Collection("meeting"),
        to={Collection("chat_message"): "user_id"},
    )
    meeting_ids = fields.NumberArrayField(
        read_only=True,
        constraints={
            "description": "Calculated. All ids from group_$_ids as integers."
        },
    )


class OrganizationTag(Model):
    collection = Collection("organization_tag")
    verbose_name = "organization tag"

    id = fields.IntegerField()
    name = fields.CharField(required=True)
    color = fields.ColorField(required=True)
    tagged_ids = fields.GenericRelationListField(
        to={
            Collection("committee"): "organization_tag_ids",
            Collection("meeting"): "organization_tag_ids",
        }
    )
    organization_id = fields.OrganizationField(
        to={Collection("organization"): "organization_tag_ids"}, required=True
    )


class Theme(Model):
    collection = Collection("theme")
    verbose_name = "theme"

    id = fields.IntegerField(required=True)
    name = fields.CharField(required=True)
    accent_100 = fields.ColorField()
    accent_200 = fields.ColorField()
    accent_300 = fields.ColorField()
    accent_400 = fields.ColorField()
    accent_50 = fields.ColorField()
    accent_500 = fields.ColorField(required=True)
    accent_600 = fields.ColorField()
    accent_700 = fields.ColorField()
    accent_800 = fields.ColorField()
    accent_900 = fields.ColorField()
    accent_a100 = fields.ColorField()
    accent_a200 = fields.ColorField()
    accent_a400 = fields.ColorField()
    accent_a700 = fields.ColorField()
    primary_100 = fields.ColorField()
    primary_200 = fields.ColorField()
    primary_300 = fields.ColorField()
    primary_400 = fields.ColorField()
    primary_50 = fields.ColorField()
    primary_500 = fields.ColorField(required=True)
    primary_600 = fields.ColorField()
    primary_700 = fields.ColorField()
    primary_800 = fields.ColorField()
    primary_900 = fields.ColorField()
    primary_a100 = fields.ColorField()
    primary_a200 = fields.ColorField()
    primary_a400 = fields.ColorField()
    primary_a700 = fields.ColorField()
    warn_100 = fields.ColorField()
    warn_200 = fields.ColorField()
    warn_300 = fields.ColorField()
    warn_400 = fields.ColorField()
    warn_50 = fields.ColorField()
    warn_500 = fields.ColorField(required=True)
    warn_600 = fields.ColorField()
    warn_700 = fields.ColorField()
    warn_800 = fields.ColorField()
    warn_900 = fields.ColorField()
    warn_a100 = fields.ColorField()
    warn_a200 = fields.ColorField()
    warn_a400 = fields.ColorField()
    warn_a700 = fields.ColorField()
    theme_for_organization_id = fields.RelationField(
        to={Collection("organization"): "theme_id"}
    )
    organization_id = fields.OrganizationField(
        to={Collection("organization"): "theme_ids"}, required=True
    )


class Committee(Model):
    collection = Collection("committee")
    verbose_name = "committee"

    id = fields.IntegerField()
    name = fields.CharField(required=True)
    description = fields.HTMLStrictField()
    meeting_ids = fields.RelationListField(
        to={Collection("meeting"): "committee_id"}, on_delete=fields.OnDelete.PROTECT
    )
    default_meeting_id = fields.RelationField(
        to={Collection("meeting"): "default_meeting_for_committee_id"}
    )
    user_ids = fields.RelationListField(
        to={Collection("user"): "committee_ids"},
        read_only=True,
        constraints={"description": "Calculated field."},
    )
    user__management_level = fields.TemplateRelationListField(
        index=5,
        to={Collection("user"): "committee_$_management_level"},
        replacement_enum=["can_manage"],
    )
    forward_to_committee_ids = fields.RelationListField(
        to={Collection("committee"): "receive_forwardings_from_committee_ids"}
    )
    receive_forwardings_from_committee_ids = fields.RelationListField(
        to={Collection("committee"): "forward_to_committee_ids"}
    )
    forwarding_user_id = fields.RelationField(
        to={Collection("user"): "forwarding_committee_ids"}
    )
    organization_tag_ids = fields.RelationListField(
        to={Collection("organization_tag"): "tagged_ids"}
    )
    organization_id = fields.OrganizationField(
        to={Collection("organization"): "committee_ids"}, required=True
    )


class Meeting(Model):
    collection = Collection("meeting")
    verbose_name = "meeting"

    id = fields.IntegerField()
    welcome_title = fields.CharField(default="Welcome to OpenSlides")
    welcome_text = fields.HTMLPermissiveField(default="Space for your welcome text.")
    name = fields.CharField(default="OpenSlides", constraints={"maxLength": 100})
    is_active_in_organization_id = fields.RelationField(
        to={Collection("organization"): "active_meeting_ids"},
        constraints={"description": "Backrelation and boolean flag at once"},
    )
    is_archived_in_organization_id = fields.RelationField(
        to={Collection("organization"): "archived_meeting_ids"},
        constraints={"description": "Backrelation and boolean flag at once"},
    )
    description = fields.CharField(
        default="Presentation and assembly system", constraints={"maxLength": 100}
    )
    location = fields.CharField()
    start_time = fields.TimestampField()
    end_time = fields.TimestampField()
    imported_at = fields.TimestampField()
    jitsi_domain = fields.CharField()
    jitsi_room_name = fields.CharField()
    jitsi_room_password = fields.CharField()
    template_for_organization_id = fields.RelationField(
        to={Collection("organization"): "template_meeting_ids"}
    )
    enable_anonymous = fields.BooleanField(default=False)
    custom_translations = fields.JSONField()
    conference_show = fields.BooleanField(default=False)
    conference_auto_connect = fields.BooleanField(default=False)
    conference_los_restriction = fields.BooleanField(default=True)
    conference_stream_url = fields.CharField()
    conference_stream_poster_url = fields.CharField()
    conference_open_microphone = fields.BooleanField(default=False)
    conference_open_video = fields.BooleanField(default=False)
    conference_auto_connect_next_speakers = fields.IntegerField(default=0)
    conference_enable_helpdesk = fields.BooleanField(default=False)
    applause_enable = fields.BooleanField(default=False)
    applause_type = fields.CharField(
        default="applause-type-bar",
        constraints={"enum": ["applause-type-bar", "applause-type-particles"]},
    )
    applause_show_level = fields.BooleanField(default=False)
    applause_min_amount = fields.IntegerField(default=1, constraints={"minimum": 0})
    applause_max_amount = fields.IntegerField(default=0, constraints={"minimum": 0})
    applause_timeout = fields.IntegerField(default=5, constraints={"minimum": 0})
    applause_particle_image_url = fields.CharField()
    projector_countdown_default_time = fields.IntegerField(required=True, default=60)
    projector_countdown_warning_time = fields.IntegerField(
        required=True, default=0, constraints={"minimum": 0}
    )
    export_csv_encoding = fields.CharField(
        default="utf-8", constraints={"enum": ["utf-8", "iso-8859-15"]}
    )
    export_csv_separator = fields.CharField(default=";")
    export_pdf_pagenumber_alignment = fields.CharField(
        default="center", constraints={"enum": ["left", "right", "center"]}
    )
    export_pdf_fontsize = fields.IntegerField(
        default=10, constraints={"enum": [10, 11, 12]}
    )
    export_pdf_line_height = fields.FloatField(
        default=1.25, constraints={"minimum": 1.0}
    )
    export_pdf_page_margin_left = fields.IntegerField(
        default=20, constraints={"minimum": 0}
    )
    export_pdf_page_margin_top = fields.IntegerField(
        default=25, constraints={"minimum": 0}
    )
    export_pdf_page_margin_right = fields.IntegerField(
        default=20, constraints={"minimum": 0}
    )
    export_pdf_page_margin_bottom = fields.IntegerField(
        default=20, constraints={"minimum": 0}
    )
    export_pdf_pagesize = fields.CharField(
        default="A4", constraints={"enum": ["A4", "A5"]}
    )
    agenda_show_subtitles = fields.BooleanField(default=False)
    agenda_enable_numbering = fields.BooleanField(default=True)
    agenda_number_prefix = fields.CharField(constraints={"maxLength": 20})
    agenda_numeral_system = fields.CharField(
        default="arabic", constraints={"enum": ["arabic", "roman"]}
    )
    agenda_item_creation = fields.CharField(
        default="default_no",
        constraints={"enum": ["always", "never", "default_yes", "default_no"]},
    )
    agenda_new_items_default_visibility = fields.CharField(
        default="internal", constraints={"enum": ["common", "internal", "hidden"]}
    )
    agenda_show_internal_items_on_projector = fields.BooleanField(default=False)
    list_of_speakers_amount_last_on_projector = fields.IntegerField(
        default=0, constraints={"minimum": -1}
    )
    list_of_speakers_amount_next_on_projector = fields.IntegerField(
        default=-1, constraints={"minimum": -1}
    )
    list_of_speakers_couple_countdown = fields.BooleanField(default=True)
    list_of_speakers_show_amount_of_speakers_on_slide = fields.BooleanField(
        default=True
    )
    list_of_speakers_present_users_only = fields.BooleanField(default=False)
    list_of_speakers_show_first_contribution = fields.BooleanField(default=False)
    list_of_speakers_enable_point_of_order_speakers = fields.BooleanField(default=True)
    list_of_speakers_enable_pro_contra_speech = fields.BooleanField(default=False)
    list_of_speakers_can_set_contribution_self = fields.BooleanField(default=False)
    list_of_speakers_speaker_note_for_everyone = fields.BooleanField(default=True)
    list_of_speakers_initially_closed = fields.BooleanField(default=False)
    motions_default_workflow_id = fields.RelationField(
        to={Collection("motion_workflow"): "default_workflow_meeting_id"}, required=True
    )
    motions_default_amendment_workflow_id = fields.RelationField(
        to={Collection("motion_workflow"): "default_amendment_workflow_meeting_id"},
        required=True,
    )
    motions_default_statute_amendment_workflow_id = fields.RelationField(
        to={
            Collection(
                "motion_workflow"
            ): "default_statute_amendment_workflow_meeting_id"
        },
        required=True,
    )
    motions_preamble = fields.TextField(default="The assembly may decide:")
    motions_default_line_numbering = fields.CharField(
        default="outside", constraints={"enum": ["outside", "inline", "none"]}
    )
    motions_line_length = fields.IntegerField(default=85, constraints={"minimum": 40})
    motions_reason_required = fields.BooleanField(default=False)
    motions_enable_text_on_projector = fields.BooleanField(default=True)
    motions_enable_reason_on_projector = fields.BooleanField(default=False)
    motions_enable_sidebox_on_projector = fields.BooleanField(default=False)
    motions_enable_recommendation_on_projector = fields.BooleanField(default=True)
    motions_show_referring_motions = fields.BooleanField(default=True)
    motions_show_sequential_number = fields.BooleanField(default=True)
    motions_recommendations_by = fields.CharField()
    motions_statute_recommendations_by = fields.CharField()
    motions_recommendation_text_mode = fields.CharField(
        default="diff", constraints={"enum": ["original", "changed", "diff", "agreed"]}
    )
    motions_default_sorting = fields.CharField(
        default="number", constraints={"enum": ["number", "weight"]}
    )
    motions_number_type = fields.CharField(
        default="per_category",
        constraints={"enum": ["per_category", "serially_numbered", "manually"]},
    )
    motions_number_min_digits = fields.IntegerField(default=2)
    motions_number_with_blank = fields.BooleanField(default=False)
    motions_statutes_enabled = fields.BooleanField(default=False)
    motions_amendments_enabled = fields.BooleanField(default=True)
    motions_amendments_in_main_list = fields.BooleanField(default=True)
    motions_amendments_of_amendments = fields.BooleanField(default=False)
    motions_amendments_prefix = fields.CharField(default="-Ä")
    motions_amendments_text_mode = fields.CharField(
        default="paragraph",
        constraints={"enum": ["freestyle", "fulltext", "paragraph"]},
    )
    motions_amendments_multiple_paragraphs = fields.BooleanField(default=True)
    motions_supporters_min_amount = fields.IntegerField(
        default=0, constraints={"minimum": 0}
    )
    motions_export_title = fields.CharField(default="Motions")
    motions_export_preamble = fields.TextField()
    motions_export_submitter_recommendation = fields.BooleanField(default=True)
    motions_export_follow_recommendation = fields.BooleanField(default=False)
    motion_poll_ballot_paper_selection = fields.CharField(
        default="CUSTOM_NUMBER",
        constraints={
            "enum": [
                "NUMBER_OF_DELEGATES",
                "NUMBER_OF_ALL_PARTICIPANTS",
                "CUSTOM_NUMBER",
            ]
        },
    )
    motion_poll_ballot_paper_number = fields.IntegerField(default=8)
    motion_poll_default_type = fields.CharField(default="pseudoanonymous")
    motion_poll_default_100_percent_base = fields.CharField(default="YNA")
    motion_poll_default_group_ids = fields.RelationListField(
        to={Collection("group"): "used_as_motion_poll_default_id"}
    )
    motion_poll_default_backend = fields.CharField(
        default="fast", constraints={"enum": ["long", "fast"]}
    )
    users_sort_by = fields.CharField(
        default="first_name",
        constraints={"enum": ["first_name", "last_name", "number"]},
    )
    users_enable_presence_view = fields.BooleanField(default=False)
    users_enable_vote_weight = fields.BooleanField(default=False)
    users_allow_self_set_present = fields.BooleanField(default=True)
    users_pdf_welcometitle = fields.CharField(default="Welcome to OpenSlides")
    users_pdf_welcometext = fields.TextField(
        default="[Place for your welcome and help text.]"
    )
    users_pdf_wlan_ssid = fields.CharField()
    users_pdf_wlan_password = fields.CharField()
    users_pdf_wlan_encryption = fields.CharField(
        constraints={"enum": ["", "WEP", "WPA", "nopass"]}
    )
    users_email_sender = fields.CharField(default="OpenSlides")
    users_email_replyto = fields.CharField()
    users_email_subject = fields.CharField(default="OpenSlides access data")
    users_email_body = fields.TextField(
        default="Dear {name},\n\nthis is your personal OpenSlides login:\n\n{url}\nUsername: {username}\nPassword: {password}\n\n\nThis email was generated automatically."
    )
    assignments_export_title = fields.CharField(default="Elections")
    assignments_export_preamble = fields.TextField()
    assignment_poll_ballot_paper_selection = fields.CharField(
        default="CUSTOM_NUMBER",
        constraints={
            "enum": [
                "NUMBER_OF_DELEGATES",
                "NUMBER_OF_ALL_PARTICIPANTS",
                "CUSTOM_NUMBER",
            ]
        },
    )
    assignment_poll_ballot_paper_number = fields.IntegerField(default=8)
    assignment_poll_add_candidates_to_list_of_speakers = fields.BooleanField(
        default=False
    )
    assignment_poll_enable_max_votes_per_option = fields.BooleanField(default=False)
    assignment_poll_sort_poll_result_by_votes = fields.BooleanField(default=True)
    assignment_poll_default_type = fields.CharField(default="pseudoanonymous")
    assignment_poll_default_method = fields.CharField(default="Y")
    assignment_poll_default_100_percent_base = fields.CharField(default="valid")
    assignment_poll_default_group_ids = fields.RelationListField(
        to={Collection("group"): "used_as_assignment_poll_default_id"}
    )
    assignment_poll_default_backend = fields.CharField(
        default="fast", constraints={"enum": ["long", "fast"]}
    )
    poll_ballot_paper_selection = fields.CharField(
        constraints={
            "enum": [
                "NUMBER_OF_DELEGATES",
                "NUMBER_OF_ALL_PARTICIPANTS",
                "CUSTOM_NUMBER",
            ]
        }
    )
    poll_ballot_paper_number = fields.IntegerField()
    poll_sort_poll_result_by_votes = fields.BooleanField()
    poll_default_type = fields.CharField(default="analog")
    poll_default_method = fields.CharField()
    poll_default_100_percent_base = fields.CharField(default="YNA")
    poll_default_group_ids = fields.RelationListField(
        to={Collection("group"): "used_as_poll_default_id"}
    )
    poll_default_backend = fields.CharField(
        default="fast", constraints={"enum": ["long", "fast"]}
    )
    poll_couple_countdown = fields.BooleanField(default=True)
    projector_ids = fields.RelationListField(
        to={Collection("projector"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    all_projection_ids = fields.RelationListField(
        to={Collection("projection"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    projector_message_ids = fields.RelationListField(
        to={Collection("projector_message"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    projector_countdown_ids = fields.RelationListField(
        to={Collection("projector_countdown"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    tag_ids = fields.RelationListField(
        to={Collection("tag"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    agenda_item_ids = fields.RelationListField(
        to={Collection("agenda_item"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    list_of_speakers_ids = fields.RelationListField(
        to={Collection("list_of_speakers"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    speaker_ids = fields.RelationListField(
        to={Collection("speaker"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    topic_ids = fields.RelationListField(
        to={Collection("topic"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    group_ids = fields.RelationListField(
        to={Collection("group"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    mediafile_ids = fields.RelationListField(
        to={Collection("mediafile"): "owner_id"}, on_delete=fields.OnDelete.CASCADE
    )
    motion_ids = fields.RelationListField(
        to={Collection("motion"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    motion_comment_section_ids = fields.RelationListField(
        to={Collection("motion_comment_section"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    motion_category_ids = fields.RelationListField(
        to={Collection("motion_category"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    motion_block_ids = fields.RelationListField(
        to={Collection("motion_block"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    motion_workflow_ids = fields.RelationListField(
        to={Collection("motion_workflow"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    motion_statute_paragraph_ids = fields.RelationListField(
        to={Collection("motion_statute_paragraph"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    motion_comment_ids = fields.RelationListField(
        to={Collection("motion_comment"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    motion_submitter_ids = fields.RelationListField(
        to={Collection("motion_submitter"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    motion_change_recommendation_ids = fields.RelationListField(
        to={Collection("motion_change_recommendation"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    motion_state_ids = fields.RelationListField(
        to={Collection("motion_state"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    poll_ids = fields.RelationListField(
        to={Collection("poll"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    option_ids = fields.RelationListField(
        to={Collection("option"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    vote_ids = fields.RelationListField(
        to={Collection("vote"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    assignment_ids = fields.RelationListField(
        to={Collection("assignment"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    assignment_candidate_ids = fields.RelationListField(
        to={Collection("assignment_candidate"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    personal_note_ids = fields.RelationListField(
        to={Collection("personal_note"): "meeting_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    chat_group_ids = fields.RelationListField(
        to={Collection("chat_group"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    chat_message_ids = fields.RelationListField(
        to={Collection("chat_message"): "meeting_id"}, on_delete=fields.OnDelete.CASCADE
    )
    logo__id = fields.TemplateRelationField(
        index=5,
        to={Collection("mediafile"): "used_as_logo_$_in_meeting_id"},
    )
    font__id = fields.TemplateRelationField(
        index=5,
        to={Collection("mediafile"): "used_as_font_$_in_meeting_id"},
    )
    committee_id = fields.RelationField(
        to={Collection("committee"): "meeting_ids"}, required=True
    )
    default_meeting_for_committee_id = fields.RelationField(
        to={Collection("committee"): "default_meeting_id"}
    )
    organization_tag_ids = fields.RelationListField(
        to={Collection("organization_tag"): "tagged_ids"}
    )
    present_user_ids = fields.RelationListField(
        to={Collection("user"): "is_present_in_meeting_ids"}
    )
    user_ids = fields.NumberArrayField(
        read_only=True,
        constraints={
            "description": "Calculated. All user ids from all users assigned to groups of this meeting."
        },
    )
    reference_projector_id = fields.RelationField(
        to={Collection("projector"): "used_as_reference_projector_meeting_id"},
        required=True,
    )
    list_of_speakers_countdown_id = fields.RelationField(
        to={
            Collection(
                "projector_countdown"
            ): "used_as_list_of_speakers_countdown_meeting_id"
        }
    )
    poll_countdown_id = fields.RelationField(
        to={Collection("projector_countdown"): "used_as_poll_countdown_meeting_id"}
    )
    default_projector__id = fields.TemplateRelationField(
        index=18,
        to={Collection("projector"): "used_as_default_$_in_meeting_id"},
        required=True,
        replacement_enum=[
            "agenda_all_items",
            "topics",
            "list_of_speakers",
            "current_list_of_speakers",
            "motion",
            "amendment",
            "motion_block",
            "assignment",
            "user",
            "mediafile",
            "projector_message",
            "projector_countdowns",
            "assignment_poll",
            "motion_poll",
            "poll",
        ],
    )
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}
    )
    default_group_id = fields.RelationField(
        to={Collection("group"): "default_group_for_meeting_id"}, required=True
    )
    admin_group_id = fields.RelationField(
        to={Collection("group"): "admin_group_for_meeting_id"}
    )


class Group(Model):
    collection = Collection("group")
    verbose_name = "group"

    id = fields.IntegerField()
    name = fields.CharField(required=True)
    permissions = fields.CharArrayField(
        in_array_constraints={
            "enum": [
                "agenda_item.can_manage",
                "agenda_item.can_see",
                "agenda_item.can_see_internal",
                "assignment.can_manage",
                "assignment.can_nominate_other",
                "assignment.can_nominate_self",
                "assignment.can_see",
                "chat.can_manage",
                "list_of_speakers.can_be_speaker",
                "list_of_speakers.can_manage",
                "list_of_speakers.can_see",
                "mediafile.can_manage",
                "mediafile.can_see",
                "meeting.can_manage_logos_and_fonts",
                "meeting.can_manage_settings",
                "meeting.can_see_autopilot",
                "meeting.can_see_frontpage",
                "meeting.can_see_history",
                "meeting.can_see_livestream",
                "motion.can_create",
                "motion.can_create_amendments",
                "motion.can_forward",
                "motion.can_manage",
                "motion.can_manage_metadata",
                "motion.can_manage_polls",
                "motion.can_see",
                "motion.can_see_internal",
                "motion.can_support",
                "poll.can_manage",
                "projector.can_manage",
                "projector.can_see",
                "tag.can_manage",
                "user.can_manage",
                "user.can_manage_presence",
                "user.can_see",
            ]
        }
    )
    weight = fields.IntegerField()
    user_ids = fields.RelationListField(to={Collection("user"): "group_$_ids"})
    default_group_for_meeting_id = fields.RelationField(
        to={Collection("meeting"): "default_group_id"},
        on_delete=fields.OnDelete.PROTECT,
    )
    admin_group_for_meeting_id = fields.RelationField(
        to={Collection("meeting"): "admin_group_id"}, on_delete=fields.OnDelete.PROTECT
    )
    mediafile_access_group_ids = fields.RelationListField(
        to={Collection("mediafile"): "access_group_ids"}, equal_fields="meeting_id"
    )
    mediafile_inherited_access_group_ids = fields.RelationListField(
        to={Collection("mediafile"): "inherited_access_group_ids"},
        read_only=True,
        constraints={"description": "Calculated field."},
    )
    read_comment_section_ids = fields.RelationListField(
        to={Collection("motion_comment_section"): "read_group_ids"},
        equal_fields="meeting_id",
    )
    write_comment_section_ids = fields.RelationListField(
        to={Collection("motion_comment_section"): "write_group_ids"},
        equal_fields="meeting_id",
    )
    read_chat_group_ids = fields.RelationListField(
        to={Collection("chat_group"): "read_group_ids"}, equal_fields="meeting_id"
    )
    write_chat_group_ids = fields.RelationListField(
        to={Collection("chat_group"): "write_group_ids"}, equal_fields="meeting_id"
    )
    poll_ids = fields.RelationListField(
        to={Collection("poll"): "entitled_group_ids"}, equal_fields="meeting_id"
    )
    used_as_motion_poll_default_id = fields.RelationField(
        to={Collection("meeting"): "motion_poll_default_group_ids"}
    )
    used_as_assignment_poll_default_id = fields.RelationField(
        to={Collection("meeting"): "assignment_poll_default_group_ids"}
    )
    used_as_poll_default_id = fields.RelationField(
        to={Collection("meeting"): "poll_default_group_ids"}
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "group_ids"}, required=True
    )


class PersonalNote(Model):
    collection = Collection("personal_note")
    verbose_name = "personal note"

    id = fields.IntegerField()
    note = fields.HTMLStrictField()
    star = fields.BooleanField()
    user_id = fields.RelationField(
        to={Collection("user"): "personal_note_$_ids"}, required=True
    )
    content_object_id = fields.GenericRelationField(
        to={Collection("motion"): "personal_note_ids"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "personal_note_ids"}, required=True
    )


class Tag(Model):
    collection = Collection("tag")
    verbose_name = "tag"

    id = fields.IntegerField()
    name = fields.CharField(required=True)
    tagged_ids = fields.GenericRelationListField(
        to={
            Collection("agenda_item"): "tag_ids",
            Collection("assignment"): "tag_ids",
            Collection("motion"): "tag_ids",
            Collection("topic"): "tag_ids",
        },
        equal_fields="meeting_id",
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "tag_ids"}, required=True
    )


class AgendaItem(Model):
    collection = Collection("agenda_item")
    verbose_name = "agenda item"

    id = fields.IntegerField()
    item_number = fields.CharField()
    comment = fields.CharField()
    closed = fields.BooleanField(default=False)
    type = fields.CharField(
        default="common", constraints={"enum": ["common", "internal", "hidden"]}
    )
    duration = fields.IntegerField(
        constraints={"description": "Given in seconds", "minimum": 0}
    )
    is_internal = fields.BooleanField(
        read_only=True, constraints={"description": "Calculated by the server"}
    )
    is_hidden = fields.BooleanField(
        read_only=True, constraints={"description": "Calculated by the server"}
    )
    level = fields.IntegerField(
        read_only=True, constraints={"description": "Calculated by the server"}
    )
    weight = fields.IntegerField(default=10000)
    content_object_id = fields.GenericRelationField(
        to={
            Collection("motion"): "agenda_item_id",
            Collection("motion_block"): "agenda_item_id",
            Collection("assignment"): "agenda_item_id",
            Collection("topic"): "agenda_item_id",
        },
        required=True,
        equal_fields="meeting_id",
    )
    parent_id = fields.RelationField(
        to={Collection("agenda_item"): "child_ids"}, equal_fields="meeting_id"
    )
    child_ids = fields.RelationListField(
        to={Collection("agenda_item"): "parent_id"}, equal_fields="meeting_id"
    )
    tag_ids = fields.RelationListField(
        to={Collection("tag"): "tagged_ids"}, equal_fields="meeting_id"
    )
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "agenda_item_ids"}, required=True
    )

    AGENDA_ITEM = "common"
    INTERNAL_ITEM = "internal"
    HIDDEN_ITEM = "hidden"


class ListOfSpeakers(Model):
    collection = Collection("list_of_speakers")
    verbose_name = "list of speakers"

    id = fields.IntegerField()
    closed = fields.BooleanField(default=False)
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    content_object_id = fields.GenericRelationField(
        to={
            Collection("motion"): "list_of_speakers_id",
            Collection("motion_block"): "list_of_speakers_id",
            Collection("assignment"): "list_of_speakers_id",
            Collection("topic"): "list_of_speakers_id",
            Collection("mediafile"): "list_of_speakers_id",
        },
        required=True,
        equal_fields="meeting_id",
    )
    speaker_ids = fields.RelationListField(
        to={Collection("speaker"): "list_of_speakers_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "list_of_speakers_ids"}, required=True
    )


class Speaker(Model):
    collection = Collection("speaker")
    verbose_name = "speaker"

    id = fields.IntegerField()
    begin_time = fields.TimestampField(read_only=True)
    end_time = fields.TimestampField(read_only=True)
    weight = fields.IntegerField(default=10000)
    speech_state = fields.CharField(
        constraints={"enum": ["contribution", "pro", "contra"]}
    )
    note = fields.CharField(constraints={"maxLength": 250})
    point_of_order = fields.BooleanField()
    list_of_speakers_id = fields.RelationField(
        to={Collection("list_of_speakers"): "speaker_ids"},
        required=True,
        equal_fields="meeting_id",
    )
    user_id = fields.RelationField(
        to={Collection("user"): "speaker_$_ids"},
        required=True,
        equal_fields="meeting_id",
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "speaker_ids"}, required=True
    )


class Topic(Model):
    collection = Collection("topic")
    verbose_name = "topic"

    id = fields.IntegerField()
    title = fields.CharField(required=True)
    text = fields.HTMLPermissiveField()
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    attachment_ids = fields.RelationListField(
        to={Collection("mediafile"): "attachment_ids"}, equal_fields="meeting_id"
    )
    agenda_item_id = fields.RelationField(
        to={Collection("agenda_item"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        required=True,
        equal_fields="meeting_id",
    )
    list_of_speakers_id = fields.RelationField(
        to={Collection("list_of_speakers"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        required=True,
        equal_fields="meeting_id",
    )
    tag_ids = fields.RelationListField(
        to={Collection("tag"): "tagged_ids"}, equal_fields="meeting_id"
    )
    poll_ids = fields.RelationListField(
        to={Collection("poll"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "topic_ids"}, required=True
    )


class Motion(Model):
    collection = Collection("motion")
    verbose_name = "motion"

    id = fields.IntegerField()
    number = fields.CharField()
    number_value = fields.IntegerField(
        read_only=True,
        constraints={
            "description": "The number value of this motion. This number is auto-generated and read-only."
        },
    )
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    title = fields.CharField(required=True)
    text = fields.HTMLStrictField()
    amendment_paragraph_ = fields.TemplateHTMLStrictField(
        index=20,
    )
    modified_final_version = fields.HTMLStrictField()
    reason = fields.HTMLStrictField()
    category_weight = fields.IntegerField(default=10000)
    state_extension = fields.CharField()
    recommendation_extension = fields.CharField()
    sort_weight = fields.IntegerField(default=10000)
    created = fields.TimestampField(read_only=True)
    last_modified = fields.TimestampField(read_only=True)
    start_line_number = fields.IntegerField(default=1, constraints={"minimum": 1})
    forwarded = fields.TimestampField(read_only=True)
    lead_motion_id = fields.RelationField(
        to={Collection("motion"): "amendment_ids"}, equal_fields="meeting_id"
    )
    amendment_ids = fields.RelationListField(
        to={Collection("motion"): "lead_motion_id"}, equal_fields="meeting_id"
    )
    sort_parent_id = fields.RelationField(
        to={Collection("motion"): "sort_child_ids"}, equal_fields="meeting_id"
    )
    sort_child_ids = fields.RelationListField(
        to={Collection("motion"): "sort_parent_id"}, equal_fields="meeting_id"
    )
    origin_id = fields.RelationField(to={Collection("motion"): "derived_motion_ids"})
    derived_motion_ids = fields.RelationListField(
        to={Collection("motion"): "origin_id"}
    )
    all_origin_ids = fields.NumberArrayField()
    all_derived_motion_ids = fields.NumberArrayField()
    state_id = fields.RelationField(
        to={Collection("motion_state"): "motion_ids"},
        required=True,
        equal_fields="meeting_id",
    )
    recommendation_id = fields.RelationField(
        to={Collection("motion_state"): "motion_recommendation_ids"},
        equal_fields="meeting_id",
    )
    recommendation_extension_reference_ids = fields.GenericRelationListField(
        to={Collection("motion"): "referenced_in_motion_recommendation_extension_ids"},
        equal_fields="meeting_id",
    )
    referenced_in_motion_recommendation_extension_ids = fields.RelationListField(
        to={Collection("motion"): "recommendation_extension_reference_ids"},
        equal_fields="meeting_id",
    )
    category_id = fields.RelationField(
        to={Collection("motion_category"): "motion_ids"}, equal_fields="meeting_id"
    )
    block_id = fields.RelationField(
        to={Collection("motion_block"): "motion_ids"}, equal_fields="meeting_id"
    )
    submitter_ids = fields.RelationListField(
        to={Collection("motion_submitter"): "motion_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    supporter_ids = fields.RelationListField(
        to={Collection("user"): "supported_motion_$_ids"}
    )
    poll_ids = fields.RelationListField(
        to={Collection("poll"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    option_ids = fields.RelationListField(
        to={Collection("option"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    change_recommendation_ids = fields.RelationListField(
        to={Collection("motion_change_recommendation"): "motion_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    statute_paragraph_id = fields.RelationField(
        to={Collection("motion_statute_paragraph"): "motion_ids"},
        equal_fields="meeting_id",
    )
    comment_ids = fields.RelationListField(
        to={Collection("motion_comment"): "motion_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    agenda_item_id = fields.RelationField(
        to={Collection("agenda_item"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    list_of_speakers_id = fields.RelationField(
        to={Collection("list_of_speakers"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        required=True,
        equal_fields="meeting_id",
    )
    tag_ids = fields.RelationListField(
        to={Collection("tag"): "tagged_ids"}, equal_fields="meeting_id"
    )
    attachment_ids = fields.RelationListField(
        to={Collection("mediafile"): "attachment_ids"}, equal_fields="meeting_id"
    )
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}, equal_fields="meeting_id"
    )
    personal_note_ids = fields.RelationListField(
        to={Collection("personal_note"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "motion_ids"}, required=True
    )


class MotionSubmitter(Model):
    collection = Collection("motion_submitter")
    verbose_name = "motion submitter"

    id = fields.IntegerField()
    weight = fields.IntegerField()
    user_id = fields.RelationField(
        to={Collection("user"): "submitted_motion_$_ids"}, required=True
    )
    motion_id = fields.RelationField(
        to={Collection("motion"): "submitter_ids"},
        required=True,
        equal_fields="meeting_id",
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "motion_submitter_ids"}, required=True
    )


class MotionComment(Model):
    collection = Collection("motion_comment")
    verbose_name = "motion comment"

    id = fields.IntegerField()
    comment = fields.HTMLStrictField()
    motion_id = fields.RelationField(
        to={Collection("motion"): "comment_ids"},
        required=True,
        equal_fields="meeting_id",
    )
    section_id = fields.RelationField(
        to={Collection("motion_comment_section"): "comment_ids"},
        required=True,
        equal_fields="meeting_id",
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "motion_comment_ids"}, required=True
    )


class MotionCommentSection(Model):
    collection = Collection("motion_comment_section")
    verbose_name = "motion comment section"

    id = fields.IntegerField()
    name = fields.CharField(required=True)
    weight = fields.IntegerField(default=10000)
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    comment_ids = fields.RelationListField(
        to={Collection("motion_comment"): "section_id"},
        on_delete=fields.OnDelete.PROTECT,
        equal_fields="meeting_id",
    )
    read_group_ids = fields.RelationListField(
        to={Collection("group"): "read_comment_section_ids"}, equal_fields="meeting_id"
    )
    write_group_ids = fields.RelationListField(
        to={Collection("group"): "write_comment_section_ids"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "motion_comment_section_ids"}, required=True
    )


class MotionCategory(Model):
    collection = Collection("motion_category")
    verbose_name = "motion category"

    id = fields.IntegerField()
    name = fields.CharField(required=True)
    prefix = fields.CharField()
    weight = fields.IntegerField(default=10000)
    level = fields.IntegerField(
        read_only=True, constraints={"description": "Calculated field."}
    )
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    parent_id = fields.RelationField(
        to={Collection("motion_category"): "child_ids"}, equal_fields="meeting_id"
    )
    child_ids = fields.RelationListField(
        to={Collection("motion_category"): "parent_id"}, equal_fields="meeting_id"
    )
    motion_ids = fields.RelationListField(
        to={Collection("motion"): "category_id"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "motion_category_ids"}, required=True
    )


class MotionBlock(Model):
    collection = Collection("motion_block")
    verbose_name = "motion block"

    id = fields.IntegerField()
    title = fields.CharField(required=True)
    internal = fields.BooleanField()
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    motion_ids = fields.RelationListField(
        to={Collection("motion"): "block_id"}, equal_fields="meeting_id"
    )
    agenda_item_id = fields.RelationField(
        to={Collection("agenda_item"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    list_of_speakers_id = fields.RelationField(
        to={Collection("list_of_speakers"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        required=True,
        equal_fields="meeting_id",
    )
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "motion_block_ids"}, required=True
    )


class MotionChangeRecommendation(Model):
    collection = Collection("motion_change_recommendation")
    verbose_name = "motion change recommendation"

    id = fields.IntegerField()
    rejected = fields.BooleanField(default=False)
    internal = fields.BooleanField(default=False)
    type = fields.CharField(
        default="replacement",
        constraints={"enum": ["replacement", "insertion", "deletion", "other"]},
    )
    other_description = fields.CharField()
    line_from = fields.IntegerField(constraints={"minimum": 0})
    line_to = fields.IntegerField(constraints={"minimum": 0})
    text = fields.HTMLStrictField()
    creation_time = fields.TimestampField(read_only=True)
    motion_id = fields.RelationField(
        to={Collection("motion"): "change_recommendation_ids"},
        required=True,
        equal_fields="meeting_id",
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "motion_change_recommendation_ids"}, required=True
    )


class MotionState(Model):
    collection = Collection("motion_state")
    verbose_name = "motion state"

    id = fields.IntegerField()
    name = fields.CharField(required=True)
    weight = fields.IntegerField(required=True)
    recommendation_label = fields.CharField()
    css_class = fields.CharField(
        required=True,
        default="lightblue",
        constraints={"enum": ["grey", "red", "green", "lightblue", "yellow"]},
    )
    restrictions = fields.CharArrayField(
        default=[],
        in_array_constraints={
            "enum": [
                "motion.can_see_internal",
                "motion.can_manage_metadata",
                "motion.can_manage",
                "is_submitter",
            ]
        },
    )
    allow_support = fields.BooleanField(default=False)
    allow_create_poll = fields.BooleanField(default=False)
    allow_submitter_edit = fields.BooleanField(default=False)
    set_number = fields.BooleanField(default=True)
    show_state_extension_field = fields.BooleanField(default=False)
    merge_amendment_into_final = fields.CharField(
        default="undefined",
        constraints={"enum": ["do_not_merge", "undefined", "do_merge"]},
    )
    show_recommendation_extension_field = fields.BooleanField(default=False)
    allow_motion_forwarding = fields.BooleanField()
    set_created_timestamp = fields.BooleanField()
    next_state_ids = fields.RelationListField(
        to={Collection("motion_state"): "previous_state_ids"},
        equal_fields=["meeting_id", "workflow_id"],
    )
    previous_state_ids = fields.RelationListField(
        to={Collection("motion_state"): "next_state_ids"},
        equal_fields=["meeting_id", "workflow_id"],
    )
    motion_ids = fields.RelationListField(
        to={Collection("motion"): "state_id"},
        on_delete=fields.OnDelete.PROTECT,
        equal_fields="meeting_id",
    )
    motion_recommendation_ids = fields.RelationListField(
        to={Collection("motion"): "recommendation_id"}, equal_fields="meeting_id"
    )
    workflow_id = fields.RelationField(
        to={Collection("motion_workflow"): "state_ids"},
        required=True,
        equal_fields="meeting_id",
    )
    first_state_of_workflow_id = fields.RelationField(
        to={Collection("motion_workflow"): "first_state_id"},
        on_delete=fields.OnDelete.PROTECT,
        equal_fields="meeting_id",
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "motion_state_ids"}, required=True
    )


class MotionWorkflow(Model):
    collection = Collection("motion_workflow")
    verbose_name = "motion workflow"

    id = fields.IntegerField()
    name = fields.CharField(required=True)
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    state_ids = fields.RelationListField(
        to={Collection("motion_state"): "workflow_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    first_state_id = fields.RelationField(
        to={Collection("motion_state"): "first_state_of_workflow_id"},
        required=True,
        equal_fields="meeting_id",
    )
    default_workflow_meeting_id = fields.RelationField(
        to={Collection("meeting"): "motions_default_workflow_id"}
    )
    default_amendment_workflow_meeting_id = fields.RelationField(
        to={Collection("meeting"): "motions_default_amendment_workflow_id"}
    )
    default_statute_amendment_workflow_meeting_id = fields.RelationField(
        to={Collection("meeting"): "motions_default_statute_amendment_workflow_id"}
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "motion_workflow_ids"}, required=True
    )


class MotionStatuteParagraph(Model):
    collection = Collection("motion_statute_paragraph")
    verbose_name = "motion statute paragraph"

    id = fields.IntegerField()
    title = fields.CharField(required=True)
    text = fields.HTMLStrictField()
    weight = fields.IntegerField(default=10000)
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    motion_ids = fields.RelationListField(
        to={Collection("motion"): "statute_paragraph_id"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "motion_statute_paragraph_ids"}, required=True
    )


class Poll(Model):
    collection = Collection("poll")
    verbose_name = "poll"

    id = fields.IntegerField()
    description = fields.TextField()
    title = fields.CharField(required=True)
    type = fields.CharField(
        required=True, constraints={"enum": ["analog", "named", "pseudoanonymous"]}
    )
    backend = fields.CharField(
        required=True, default="fast", constraints={"enum": ["long", "fast"]}
    )
    is_pseudoanonymized = fields.BooleanField()
    pollmethod = fields.CharField(
        required=True, constraints={"enum": ["Y", "YN", "YNA", "N"]}
    )
    state = fields.CharField(
        default="created",
        constraints={"enum": ["created", "started", "finished", "published"]},
    )
    min_votes_amount = fields.IntegerField(default=1, constraints={"minimum": 1})
    max_votes_amount = fields.IntegerField(default=1, constraints={"minimum": 1})
    max_votes_per_option = fields.IntegerField(default=1, constraints={"minimum": 1})
    global_yes = fields.BooleanField(default=False)
    global_no = fields.BooleanField(default=False)
    global_abstain = fields.BooleanField(default=False)
    onehundred_percent_base = fields.CharField(
        required=True,
        default="disabled",
        constraints={
            "enum": ["Y", "YN", "YNA", "N", "valid", "cast", "entitled", "disabled"]
        },
    )
    votesvalid = fields.DecimalField()
    votesinvalid = fields.DecimalField()
    votescast = fields.DecimalField()
    entitled_users_at_stop = fields.JSONField()
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    content_object_id = fields.GenericRelationField(
        to={
            Collection("motion"): "poll_ids",
            Collection("assignment"): "poll_ids",
            Collection("topic"): "poll_ids",
        },
        required=True,
        equal_fields="meeting_id",
    )
    option_ids = fields.RelationListField(
        to={Collection("option"): "poll_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    global_option_id = fields.RelationField(
        to={Collection("option"): "used_as_global_option_in_poll_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    voted_ids = fields.RelationListField(to={Collection("user"): "poll_voted_$_ids"})
    entitled_group_ids = fields.RelationListField(
        to={Collection("group"): "poll_ids"}, equal_fields="meeting_id"
    )
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "poll_ids"}, required=True
    )

    STATE_CREATED = "created"
    STATE_STARTED = "started"
    STATE_FINISHED = "finished"
    STATE_PUBLISHED = "published"

    TYPE_ANALOG = "analog"
    TYPE_NAMED = "named"
    TYPE_PSEUDOANONYMOUS = "pseudoanonymous"


class Option(Model):
    collection = Collection("option")
    verbose_name = "option"

    id = fields.IntegerField()
    weight = fields.IntegerField(default=10000)
    text = fields.HTMLStrictField()
    yes = fields.DecimalField()
    no = fields.DecimalField()
    abstain = fields.DecimalField()
    poll_id = fields.RelationField(
        to={Collection("poll"): "option_ids"}, equal_fields="meeting_id"
    )
    used_as_global_option_in_poll_id = fields.RelationField(
        to={Collection("poll"): "global_option_id"}, equal_fields="meeting_id"
    )
    vote_ids = fields.RelationListField(
        to={Collection("vote"): "option_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    content_object_id = fields.GenericRelationField(
        to={Collection("user"): "option_$_ids", Collection("motion"): "option_ids"},
        equal_fields="meeting_id",
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "option_ids"}, required=True
    )


class Vote(Model):
    collection = Collection("vote")
    verbose_name = "vote"

    id = fields.IntegerField()
    weight = fields.DecimalField()
    value = fields.CharField()
    user_token = fields.CharField(required=True)
    option_id = fields.RelationField(
        to={Collection("option"): "vote_ids"}, required=True, equal_fields="meeting_id"
    )
    user_id = fields.RelationField(to={Collection("user"): "vote_$_ids"})
    delegated_user_id = fields.RelationField(
        to={Collection("user"): "vote_delegated_vote_$_ids"}
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "vote_ids"}, required=True
    )


class Assignment(Model):
    collection = Collection("assignment")
    verbose_name = "assignment"

    id = fields.IntegerField()
    title = fields.CharField(required=True)
    description = fields.HTMLStrictField()
    open_posts = fields.IntegerField(default=0, constraints={"minimum": 0})
    phase = fields.CharField(
        default="search", constraints={"enum": ["search", "voting", "finished"]}
    )
    default_poll_description = fields.TextField()
    number_poll_candidates = fields.BooleanField()
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    candidate_ids = fields.RelationListField(
        to={Collection("assignment_candidate"): "assignment_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    poll_ids = fields.RelationListField(
        to={Collection("poll"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    agenda_item_id = fields.RelationField(
        to={Collection("agenda_item"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    list_of_speakers_id = fields.RelationField(
        to={Collection("list_of_speakers"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
        required=True,
        equal_fields="meeting_id",
    )
    tag_ids = fields.RelationListField(
        to={Collection("tag"): "tagged_ids"}, equal_fields="meeting_id"
    )
    attachment_ids = fields.RelationListField(
        to={Collection("mediafile"): "attachment_ids"}, equal_fields="meeting_id"
    )
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "assignment_ids"}, required=True
    )


class AssignmentCandidate(Model):
    collection = Collection("assignment_candidate")
    verbose_name = "assignment candidate"

    id = fields.IntegerField()
    weight = fields.IntegerField(default=10000)
    assignment_id = fields.RelationField(
        to={Collection("assignment"): "candidate_ids"},
        required=True,
        equal_fields="meeting_id",
    )
    user_id = fields.RelationField(
        to={Collection("user"): "assignment_candidate_$_ids"}, required=True
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "assignment_candidate_ids"}, required=True
    )


class Mediafile(Model):
    collection = Collection("mediafile")
    verbose_name = "mediafile"

    id = fields.IntegerField()
    title = fields.CharField(
        constraints={"description": "Title and parent_id must be unique."}
    )
    is_directory = fields.BooleanField()
    filesize = fields.IntegerField(
        read_only=True,
        constraints={"description": "In bytes, not the human readable format anymore."},
    )
    filename = fields.CharField(
        constraints={
            "description": "The uploaded filename. Will be used for downloading. Only writeable on create."
        }
    )
    mimetype = fields.CharField()
    pdf_information = fields.JSONField()
    create_timestamp = fields.TimestampField()
    is_public = fields.BooleanField(
        required=True,
        read_only=True,
        constraints={
            "description": "Calculated field. inherited_access_group_ids == [] can have two causes: cancelling access groups (=> is_public := false) or no access groups at all (=> is_public := true)"
        },
    )
    token = fields.CharField()
    inherited_access_group_ids = fields.RelationListField(
        to={Collection("group"): "mediafile_inherited_access_group_ids"},
        read_only=True,
        constraints={"description": "Calculated field."},
    )
    access_group_ids = fields.RelationListField(
        to={Collection("group"): "mediafile_access_group_ids"}
    )
    parent_id = fields.RelationField(
        to={Collection("mediafile"): "child_ids"}, equal_fields="owner_id"
    )
    child_ids = fields.RelationListField(
        to={Collection("mediafile"): "parent_id"}, equal_fields="owner_id"
    )
    list_of_speakers_id = fields.RelationField(
        to={Collection("list_of_speakers"): "content_object_id"},
        on_delete=fields.OnDelete.CASCADE,
    )
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}
    )
    attachment_ids = fields.GenericRelationListField(
        to={
            Collection("motion"): "attachment_ids",
            Collection("topic"): "attachment_ids",
            Collection("assignment"): "attachment_ids",
        }
    )
    owner_id = fields.GenericRelationField(
        to={
            Collection("organization"): "mediafile_ids",
            Collection("meeting"): "mediafile_ids",
        },
        required=True,
    )
    used_as_logo__in_meeting_id = fields.TemplateRelationField(
        index=13,
        to={Collection("meeting"): "logo_$_id"},
    )
    used_as_font__in_meeting_id = fields.TemplateRelationField(
        index=13,
        to={Collection("meeting"): "font_$_id"},
    )


class Projector(Model):
    collection = Collection("projector")
    verbose_name = "projector"

    id = fields.IntegerField()
    name = fields.CharField()
    scale = fields.IntegerField(default=0)
    scroll = fields.IntegerField(default=0)
    width = fields.IntegerField(default=1200, constraints={"minimum": 1})
    aspect_ratio_numerator = fields.IntegerField(default=16, constraints={"minimum": 1})
    aspect_ratio_denominator = fields.IntegerField(
        default=9, constraints={"minimum": 1}
    )
    color = fields.ColorField(default="#000000")
    background_color = fields.ColorField(default="#ffffff")
    header_background_color = fields.ColorField(default="#317796")
    header_font_color = fields.ColorField(default="#f5f5f5")
    header_h1_color = fields.ColorField(default="#317796")
    chyron_background_color = fields.ColorField(default="#317796")
    chyron_font_color = fields.ColorField(default="#ffffff")
    show_header_footer = fields.BooleanField(default=True)
    show_title = fields.BooleanField(default=True)
    show_logo = fields.BooleanField(default=True)
    show_clock = fields.BooleanField(default=True)
    sequential_number = fields.IntegerField(
        required=True,
        read_only=True,
        constraints={
            "description": "The (positive) serial number of this motion. This number is auto-generated and read-only."
        },
    )
    current_projection_ids = fields.RelationListField(
        to={Collection("projection"): "current_projector_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    preview_projection_ids = fields.RelationListField(
        to={Collection("projection"): "preview_projector_id"}, equal_fields="meeting_id"
    )
    history_projection_ids = fields.RelationListField(
        to={Collection("projection"): "history_projector_id"}, equal_fields="meeting_id"
    )
    used_as_reference_projector_meeting_id = fields.RelationField(
        to={Collection("meeting"): "reference_projector_id"}
    )
    used_as_default__in_meeting_id = fields.TemplateRelationField(
        index=16,
        to={Collection("meeting"): "default_projector_$_id"},
        replacement_enum=[
            "agenda_all_items",
            "topics",
            "list_of_speakers",
            "current_list_of_speakers",
            "motion",
            "amendment",
            "motion_block",
            "assignment",
            "user",
            "mediafile",
            "projector_message",
            "projector_countdowns",
            "assignment_poll",
            "motion_poll",
            "poll",
        ],
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "projector_ids"}, required=True
    )


class Projection(Model):
    collection = Collection("projection")
    verbose_name = "projection"

    id = fields.IntegerField()
    options = fields.JSONField()
    stable = fields.BooleanField(default=False)
    weight = fields.IntegerField()
    type = fields.CharField()
    current_projector_id = fields.RelationField(
        to={Collection("projector"): "current_projection_ids"},
        equal_fields="meeting_id",
    )
    preview_projector_id = fields.RelationField(
        to={Collection("projector"): "preview_projection_ids"},
        equal_fields="meeting_id",
    )
    history_projector_id = fields.RelationField(
        to={Collection("projector"): "history_projection_ids"},
        equal_fields="meeting_id",
    )
    content_object_id = fields.GenericRelationField(
        to={
            Collection("user"): "projection_$_ids",
            Collection("projector_countdown"): "projection_ids",
            Collection("projector_message"): "projection_ids",
            Collection("poll"): "projection_ids",
            Collection("topic"): "projection_ids",
            Collection("agenda_item"): "projection_ids",
            Collection("assignment"): "projection_ids",
            Collection("motion_block"): "projection_ids",
            Collection("list_of_speakers"): "projection_ids",
            Collection("mediafile"): "projection_ids",
            Collection("motion"): "projection_ids",
            Collection("meeting"): "projection_ids",
        },
        equal_fields="meeting_id",
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "all_projection_ids"}, required=True
    )


class ProjectorMessage(Model):
    collection = Collection("projector_message")
    verbose_name = "projector message"

    id = fields.IntegerField()
    message = fields.HTMLStrictField()
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "projector_message_ids"}, required=True
    )


class ProjectorCountdown(Model):
    collection = Collection("projector_countdown")
    verbose_name = "projector countdown"

    id = fields.IntegerField()
    title = fields.CharField(required=True)
    description = fields.CharField(default="")
    default_time = fields.IntegerField()
    countdown_time = fields.FloatField(default=60)
    running = fields.BooleanField(default=False)
    projection_ids = fields.RelationListField(
        to={Collection("projection"): "content_object_id"}, equal_fields="meeting_id"
    )
    used_as_list_of_speakers_countdown_meeting_id = fields.RelationField(
        to={Collection("meeting"): "list_of_speakers_countdown_id"}
    )
    used_as_poll_countdown_meeting_id = fields.RelationField(
        to={Collection("meeting"): "poll_countdown_id"}
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "projector_countdown_ids"}, required=True
    )


class ChatGroup(Model):
    collection = Collection("chat_group")
    verbose_name = "chat group"

    id = fields.IntegerField()
    name = fields.CharField(required=True)
    weight = fields.IntegerField(default=10000)
    chat_message_ids = fields.RelationListField(
        to={Collection("chat_message"): "chat_group_id"},
        on_delete=fields.OnDelete.CASCADE,
        equal_fields="meeting_id",
    )
    read_group_ids = fields.RelationListField(
        to={Collection("group"): "read_chat_group_ids"}, equal_fields="meeting_id"
    )
    write_group_ids = fields.RelationListField(
        to={Collection("group"): "write_chat_group_ids"}, equal_fields="meeting_id"
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "chat_group_ids"}, required=True
    )


class ChatMessage(Model):
    collection = Collection("chat_message")
    verbose_name = "chat message"

    id = fields.IntegerField()
    content = fields.HTMLStrictField(required=True)
    created = fields.TimestampField(required=True)
    user_id = fields.RelationField(
        to={Collection("user"): "chat_message_$_ids"}, required=True
    )
    chat_group_id = fields.RelationField(
        to={Collection("chat_group"): "chat_message_ids"}, required=True
    )
    meeting_id = fields.RelationField(
        to={Collection("meeting"): "chat_message_ids"}, required=True
    )
