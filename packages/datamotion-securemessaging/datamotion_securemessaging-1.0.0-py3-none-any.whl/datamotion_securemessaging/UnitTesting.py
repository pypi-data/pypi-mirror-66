import requests, http, json
from datamotion_securemessaging.SecureMessaging import Secure
from datamotion_securemessaging.Models.Accounts import LogOnRequest, ChangePasswordRequest
from datamotion_securemessaging.Models.Folders import NewFolderRequest
from datamotion_securemessaging.Models.Messages import MessageIdsRequest, SummariesRequest, SearchRequest, SendRequest, SendMimeRequest, MoveRequest, SummariesWithMetaRequest, SaveDraftRequest, Attachment
import unittest
from unittest.mock import patch

class Context:
    secure = Secure('https://sandbox.datamotion.com/SecureMessagingAPI')
    user = LogOnRequest()
    password = ChangePasswordRequest()
    newfolder = NewFolderRequest()
    MIDs = MessageIdsRequest()
    summaries = SummariesRequest()
    search = SearchRequest()
    send = SendRequest()
    mime = SendMimeRequest()
    move = MoveRequest()
    summswithmeta = SummariesWithMetaRequest()
    draft = SaveDraftRequest()
    FID = ''
    MID = ''
    MimeMessage = ''
    CreatedFolderId = None

# No Session Key Tests
class TestSecureMethods(unittest.TestCase):
    def test_LogOnEmptyFields(self):
        try:
            resp = Context.secure.Account.GetSessionKey(Context.user)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_LogOnOnlyUserIdOrEmail(self):
        Context.user.UserIdOrEmail = 'username'
        Context.user.Password = None
        try:
            resp = Context.secure.Account.GetSessionKey(Context.user)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_LogOnOnlyPassword(self):
        Context.user.UserIdOrEmail = None
        Context.user.Password = 'password'
        try:
            resp = Context.secure.Account.GetSessionKey(Context.user)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_LogOnInvalidFields(self):
        Context.user.UserIdOrEmail = 'username'
        Context.user.Password = 'password'
        try:
            resp = Context.secure.Account.GetSessionKey(Context.user)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_DetailsNoSessionKey(self):
        try:
            resp = Context.secure.Account.GetAccountDetails()
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_ChangePasswordNoSessionKey(self):
        Context.password.OldPassword = 'OldPassword'
        Context.password.NewPassword = 'NewPassword'
        try:
            resp = Context.secure.Account.ChangePassword(Context.password)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_LogoutNoSessionKey(self):
        try:
            resp = Context.secure.Account.Logout()
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_ListFoldersNoSessionKey(self):
        try:
            resp = Context.secure.Folder.ListFolders()
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_CreateFolderNoSessionKey(self):
        Context.newfolder.FolderName = 'TestFolder'
        try:
            resp = Context.secure.Folder.CreateNewFolder(Context.newfolder)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_DeleteFolderNoSessionKey(self):
        try:
            resp = Context.secure.Folder.DeleteFolder('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMessageIdsNoSessionKey(self):
        try:
            resp = Context.secure.Message.GetMessageIds(MessageIdsRequest())
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMessageSummariesNoSessionKey(self):
        Context.summaries.LastMessageIDReceived = 0
        try:
            resp = Context.secure.Message.GetMessageSummaries(Context.summaries)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetUnreadMessagesNoSessionKey(self):
        try:
            resp = Context.secure.Message.GetUnreadMessages()
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_SearchInboxNoSessionKey(self):
        Context.search.PageNum = 1
        Context.search.PageSize = 10
        try:
            resp = Context.secure.Message.SearchInbox(Context.search)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMessageMetadataNoSessionKey(self):
        try:
            resp = Context.secure.Message.GetMessageMetadata('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMessageNoSessionKey(self):
        try:
            resp = Context.secure.Message.GetMessage('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMimeMessageNoSessionKey(self):
        try:
            resp = Context.secure.Message.GetMimeMessage('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_SendMessageNoSessionKey(self):
        try:
            resp = Context.secure.Message.SendMessage(Context.send)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_SendMimeMessageNoSessionKey(self):
        Context.mime.MimeMessage = 'test'
        try:
            resp = Context.secure.Message.SendMimeMessage(Context.mime)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_MoveMessageNoSessionKey(self):
        Context.move.DestinationFolderId = 123
        try:
            resp = Context.secure.Message.MoveMessage('12345', Context.move)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_DeleteMessageNoSessionKey(self):
        try:
            resp = Context.secure.Message.DeleteMessage('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_RetractMessageNoSessionKey(self):
        try:
            resp = Context.secure.Message.RetractMessage('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))
    
    def test_NoAttachmentDataNoSessionKey(self):
        try:
            resp = Context.secure.Message.NoAttachmentData('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetAttachmentNoSessionKey(self):
        try:
            resp = Context.secure.Message.GetAttachment('1234')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetSummariesWithMetaNoSessionKey(self):
        Context.summswithmeta.LastMessageIDReceived = 0
        try:
            resp = Context.secure.Message.GetSummariesWithMeta(Context.summswithmeta)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_SaveDraftNoSessionKey(self):
        Context.draft.To.clear()
        try:
            resp = Context.secure.Message.SaveDraft(Context.draft)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_SendDraftNoSessionKey(self):
        try:
            resp = Context.secure.Message.SendDraft('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

# Positive Tests
class TestSecureMethods2(unittest.TestCase):
    def test_ALogOnPositive(self):
        Context.user.UserIdOrEmail = 'user1@dmweb.citest.com'
        Context.user.Password = 'P@##w0rd'
        Context.secure.Account.GetSessionKey(Context.user)

    def test_DetailsPositive(self):
        Context.secure.Account.GetAccountDetails()

    @unittest.skip("Avoid Changing Password")
    def test_ChangePasswordPositive(self):
        Context.password.OldPassword = Context.user.Password
        Context.password.NewPassword = 'NewPassword'
        Context.secure.Account.ChangePassword(Context.password)

    def test_ZLogoutPositive(self):
        Context.secure.Account.Logout()

    def test_ListFoldersPositive(self):
        Context.secure.Folder.ListFolders()

    def test_CreateFolderPositive(self):
        Context.newfolder.FolderName = 'NewFolder'
        CreatedFolderId = Context.secure.Folder.CreateNewFolder(Context.newfolder)
        Context.CreatedFolderId = str(CreatedFolderId['FolderId'])

    def test_DeleteFolderPositive(self):
        Context.secure.Folder.DeleteFolder(Context.CreatedFolderId)

    def test_GetMessageIdsPositive(self):
        Context.secure.Message.GetMessageIds() 

    def test_GetMessageSummariesPositive(self):
        Context.summaries.LastMessageIDReceived = 0
        Context.secure.Message.GetMessageSummaries(Context.summaries)

    def test_GetUnreadMessagesPositive(self):
        Context.secure.Message.GetUnreadMessages()

    def test_SearchInboxPositive(self):
        Context.search.PageNum = 1
        Context.search.PageSize = 10
        Context.secure.Message.SearchInbox(Context.search)

    def test_GetMessageMetadataPositive(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        mid = Context.secure.Message.SendMessage(Context.send)
        Context.secure.Message.GetMessageMetadata(str(mid['MessageId']))

    def test_GetMessagePositive(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        mid = Context.secure.Message.SendMessage(Context.send)
        Context.secure.Message.GetMessage(str(mid['MessageId']))

    def test_GetMimeMessagePositive(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        mid = Context.secure.Message.SendMessage(Context.send)
        Context.secure.Message.GetMimeMessage(str(mid['MessageId']))

    def test_SendMessagePositive(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        Context.send.Subject = 'Test Message Send Message'
        Context.secure.Message.SendMessage(Context.send)

    def test_SendMimeMessagePositive(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        Context.send.Subject = ''
        mid = Context.secure.Message.SendMessage(Context.send)
        mime = Context.secure.Message.GetMimeMessage(str(mid['MessageId']))
        Context.MimeMessage = str(mime['MimeMessage'])
        Context.mime.MimeMessage = Context.MimeMessage
        Context.secure.Message.SendMimeMessage(Context.mime)

    def test_MoveMessagePositive(self):
        Context.FID = Context.secure.Folder.CreateNewFolder(Context.newfolder)
        Context.move.DestinationFolderId = Context.FID
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        mid = Context.secure.Message.SendMessage(Context.send)
        Context.secure.Message.MoveMessage(str(mid['MessageId']), Context.move)
        Context.secure.Folder.DeleteFolder(str(Context.FID['FolderId']))

    def test_DeleteMessagePositive(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        mid = Context.secure.Message.SendMessage(Context.send)
        Context.secure.Message.DeleteMessage(str(mid['MessageId']))

    def test_RetractMessagePositive(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        mid = Context.secure.Message.SendMessage(Context.send)
        Context.secure.Message.RetractMessage(str(mid['MessageId']))
    
    def test_NoAttachmentDataPositive(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        mid = Context.secure.Message.SendMessage(Context.send)
        Context.secure.Message.NoAttachmentData(str(mid['MessageId']))

    def test_GetAttachmentPositive(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        mid = Context.secure.Message.SendMessage(Context.send)
        Context.secure.Message.GetAttachment(str(mid['MessageId']))

    def test_GetSummariesWithMetaPositive(self):
        Context.summswithmeta.LastMessageIDReceived = 0
        Context.secure.Message.GetSummariesWithMeta(Context.summswithmeta)

    def test_SaveDraftPositive(self):
        Context.draft.To.clear()
        Context.draft.To.append('user2@dmweb.citest.com')
        Context.draft.Subject = 'Test Message Save Draft'
        Context.secure.Message.SaveDraft(Context.draft)

    def test_SendDraftPositive(self):
        Context.draft.To.clear()
        Context.draft.To.append('user2@dmweb.citest.com')
        Context.draft.Subject = 'Test Message Send Draft'
        mid = Context.secure.Message.SaveDraft(Context.draft)
        Context.secure.Message.SendDraft(str(mid['MessageId']))

# Error Tests
class TestSecureMethods3(unittest.TestCase):
    def test_CreateFolderEmptyFields(self):
        Context.newfolder.FolderName = None
        Context.newfolder.FolderType = None
        try:
            resp = Context.secure.Folder.CreateNewFolder(Context.newfolder)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_CreateFolderOnlyFolderName(self):
        Context.newfolder.FolderName = 'NewFolder'
        Context.newfolder.FolderType = None
        try:
            resp = Context.secure.Folder.CreateNewFolder(Context.newfolder)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_CreateFolderFalseFolderID(self):
        Context.newfolder.FolderName = 'NewFolder'
        Context.newfolder.FolderType = 12345
        try:
            resp = Context.secure.Folder.CreateNewFolder(Context.newfolder)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_DeleteFolderInvalidFolderID(self):
        try:
            resp = Context.secure.Folder.DeleteFolder('1234')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMessageIdsEmptyFields(self):
        Context.MIDs.FolderId = None
        Context.MIDs.MessageListFilter = None
        Context.MIDs.MustHaveAttachments = None
        try:
            resp = Context.secure.Message.GetMessageIds(Context.MIDs)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_GetMessageIdsInvalidFolderId(self):
        Context.MIDs.FolderId = 123
        Context.MIDs.MessageListFilter = 0
        Context.MIDs.MustHaveAttachments = False
        try:
            resp = Context.secure.Message.GetMessageIds(Context.MIDs)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMessageIdsNotInbox(self):
        Context.MIDs.FolderId = 3
        Context.MIDs.MessageListFilter = 0
        Context.MIDs.MustHaveAttachments = False
        try:
            resp = Context.secure.Message.GetMessageIds(Context.MIDs)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMessageIdsFalseMLF(self):
        Context.MIDs.FolderId = 1
        Context.MIDs.MessageListFilter = 123
        Context.MIDs.MustHaveAttachments = False
        try:
            resp = Context.secure.Message.GetMessageIds(Context.MIDs)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMessageSummariesNoFID(self):
        Context.summaries.FolderId = None
        try:
            resp = Context.secure.Message.GetMessageSummaries(Context.summaries)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_SearchInboxNoFID(self):
        Context.search.FolderId = None
        try:
            resp = Context.secure.Message.SearchInbox(Context.search)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_SearchInboxNotInbox(self):
        Context.search.FolderId = 3
        try:
            resp = Context.secure.Message.SearchInbox(Context.search)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_SearchInboxInvalidPageNum(self):
        Context.search.FolderId = 1
        Context.search.PageNum = 1001
        try:
            resp = Context.secure.Message.SearchInbox(Context.search)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_SearchInboxNoPageNum(self):
        Context.search.FolderId = 1
        Context.search.PageNum = None
        try:
            resp = Context.secure.Message.SearchInbox(Context.search)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_SearchInboxNoPageSize(self):
        Context.search.FolderId = 1
        Context.search.PageNum = 1
        Context.search.PageSize = None
        try:
            resp = Context.secure.Message.SearchInbox(Context.search)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_GetMessageMetadataInvalidMID(self):
        try:
            resp = Context.secure.Message.GetMessageMetadata('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMessageInvalidMID(self):
        try:
            resp = Context.secure.Message.GetMessage('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_GetMimeMessageInvalidMID(self):
        try:
            resp = Context.secure.Message.GetMimeMessage('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_SendMessageNoToField(self):
        Context.send.To.clear()
        try:
            resp = Context.secure.Message.SendMessage(Context.send)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_SendMessageInvalidToField(self):
        Context.send.To.clear()
        Context.send.To.append('testemail')
        try:
            resp = Context.secure.Message.SendMessage(Context.send)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_SendMessageInvalidCcField(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        Context.send.Cc = 'testemail'
        try:
            resp = Context.secure.Message.SendMessage(Context.send)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_SendMessageInvalidBccField(self):
        Context.send.To.clear()
        Context.send.To.append('user2@dmweb.citest.com')
        Context.send.Cc = 'testemail'
        Context.send.Bcc = 'testemail'
        try:
            resp = Context.secure.Message.SendMessage(Context.send)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_SendMimeMessageInvalidMimeString(self):
        Context.mime.MimeMessage = 'TestMime'
        try:
            resp = Context.secure.Message.SendMimeMessage(Context.mime)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_MoveMessageInvalidMID(self):
        Context.move.DestinationFolderId = 1
        try:
            resp = Context.secure.Message.MoveMessage('12345', Context.move)
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_MoveMessageInvalidDestinationFID(self):
        Context.move.DestinationFolderId = None
        try:
            resp = Context.secure.Message.MoveMessage('12345', Context.move)
        except Exception:
            self.assertTrue(resp.__contains__('400'))

    def test_DeleteMessageInvalidMID(self):
        try:
            resp = Context.secure.Message.DeleteMessage('12345')
        except Exception:
            self.assertTrue(resp.__contains__('401'))

    def test_RetractMessageInvalidMID(self):
        try:
            resp = Context.secure.Message.RetractMessage('12345')
        except Exception:
            self.assertTrue(resp.__contains__('400'))

if __name__ == '__main__':
    unittest.main()
