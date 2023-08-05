class MessageIdsRequest:
    FolderId = 1
    MessageListFilter = 0
    MustHaveAttachments = False

class SummariesRequest:
    FolderId = 1
    LastMessageIDReceived = None

class UnreadRequest:
    None

class SearchRequest:
    Filter = None
    FolderId = 1
    GetInboxUnReadOnly = False
    GetRetractedMsgs = False
    OrderBy = None
    OrderDesc = False
    PageNum = None
    PageSize = None

class GetMetadataRequest:
    None

class GetMessageRequest:
    None

class GetMimeRequest:
    None

class Attachment:
    def __init__(self, AttachmentBase64, ContentId, ContentType, FileName):
        self.AttachmentBase64 = AttachmentBase64
        self.ContentId = ContentId
        self.ContentType = ContentType
        self.FileName = FileName

class SendRequest:
    To = [None]
    From = None
    Cc = [None]
    Bcc = [None]
    Subject = None
    CreateTime = None
    Attachments = []
    AttachmentBase64 = None
    ContentId = None
    ContentType = None
    FileName = None
    HtmlBody = None
    TextBody = None
    
class SendMimeRequest:
    MimeMessage = None

class MoveRequest:
    DestinationFolderId = None

class DeleteMessageRequest:
    None

class RetractRequest:
    None

class NoAttachmentRequest:
    None

class GetAttachmentRequest:
    None

class SummariesWithMetaRequest:
    FolderId = 1
    LastMessageIDReceived = None

class SaveDraftRequest:
    To = [None]
    From = None
    Cc = [None]
    Bcc = [None]
    Subject = None
    CreateTime = None
    Attachments = []
    AttachmentBase64 = None
    ContentId = None
    ContentType = None
    FileName = None
    HtmlBody = None
    TextBody = None

class SendDraftRequest:
    None