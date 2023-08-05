import requests
import http
import json
from .Models.Accounts import LogOnRequest, ChangePasswordRequest
from .Models.Folders import NewFolderRequest
from .Models.Messages import MessageIdsRequest, SummariesRequest, SearchRequest, SendRequest, SendMimeRequest, MoveRequest, SummariesWithMetaRequest, SaveDraftRequest, Attachment

# Initialize baseurl to an empty string
baseurl = ''

# Creates a new Requests Session
client = requests.Session()
# Adds a Content-Type header with the value application/json
client.headers.update({'Content-Type': 'application/json'})

class Secure:
    # Constructor that sets baseurl to either 'https://ssl.datamotion.com/SecureMessagingAPI' 
    # or a user defined url based on the input that it receives
    def __init__(self, url=None):
        if url == None:
            Secure.baseurl = 'https://ssl.datamotion.com/SecureMessagingAPI'
        else:
            Secure.baseurl = url
            
    class Account:
        # Takes as input a LogOnRequest Model and retrieves a session key for the user
        @staticmethod
        def GetSessionKey(user = LogOnRequest()):
            # Creates a dictionary with the information from the model
            d={'UserIdOrEmail': user.UserIdOrEmail, 'Password': user.Password}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Account/Logon', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                # Adds the session key as a header for all subsequent requests
                SessionKey = res.get('SessionKey')
                client.headers.update({'X-Session-Key': SessionKey})
                return(res)
            else:
                return(response.text)

        # Displays account details to the user
        @staticmethod
        def GetAccountDetails():
            # Makes the HTTP request
            response = client.get(Secure.baseurl+'/Account/Details', verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a ChangePasswordRequest Model and changes the user's password
        @staticmethod
        def ChangePassword(password = ChangePasswordRequest()):
            # Creates a dictionary with the information from the model
            d={'OldPassword': password.OldPassword, 'NewPassword': password.NewPassword}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Account/ChangePassword', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                return(response.text)
            else:
                return(response.text)

        # Logs the user out of their session
        @staticmethod
        def Logout():
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Account/Logout', verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                return(response.text)
            else:
                return(response.text)

    class Folder:
        # Displays the details of the folders on the user's account
        @staticmethod
        def ListFolders():
            # Makes the HTTP request
            response = client.get(Secure.baseurl+'/Folder/List', verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a NewFolderRequest Model and creates a new folder in the user's account
        @staticmethod
        def CreateNewFolder(newFolder = NewFolderRequest()):
            # Creates a dictionary with the information from the model
            d={'FolderName': newFolder.FolderName, 'FolderType': newFolder.FolderType}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Folder', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a FolderId string and deletes that folder from the user's account
        @staticmethod
        def DeleteFolder(FolderId):
            # Makes the HTTP request
            response = client.delete(Secure.baseurl+'/Folder/'+FolderId, verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                return(response.text)
            else:
                return(response.text)

    class Message:
        # Takes as input a MessageIdsRequest Model and displays the message ids from a given folder
        @staticmethod
        def GetMessageIds(messageIds = MessageIdsRequest()):
            # Creates a dictionary with the information from the model
            d={'FolderId': messageIds.FolderId, 'MessageListFilter': messageIds.MessageListFilter, 'MustHaveAttachments': messageIds.MustHaveAttachments}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Message/GetInboxMessageIds', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a SummariesRequest Model and the message summaries for the messages in a given folder
        @staticmethod
        def GetMessageSummaries(summaries = SummariesRequest()):
            # Creates a dictionary with the information from the model
            d={'FolderId': summaries.FolderId, 'LastMessageIDReceived': summaries.LastMessageIDReceived}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Message/GetMessageSummaries', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)
                
        # Displays all of the unread messages in the user's inbox
        @staticmethod
        def GetUnreadMessages():
            # Makes the HTTP request
            response = client.get(Secure.baseurl+'/Message/Inbox/Unread', verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a SearchRequest Model and searches the user's inbox based on the given filter parameters
        @staticmethod
        def SearchInbox(search = SearchRequest()):
            # Creates a dictionary with the information from the model
            d={'Filter': search.Filter, 'FolderId': search.FolderId, 'GetInboxUnReadOnly': search.GetInboxUnReadOnly, 'GetRetractedMsgs': search.GetRetractedMsgs, 'OrderBy': search.OrderBy, 'OrderDesc': search.OrderDesc, 'PageNum': search.PageNum, 'PageSize': search.PageSize}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Message/Inbox/Search', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a MessageId string and displays the metadata for that message
        @staticmethod
        def GetMessageMetadata(MessageId):
            # Makes the HTTP request
            response = client.get(Secure.baseurl+'/Message/'+MessageId+'/Metadata', verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a MessageId string and displays the details of that message
        @staticmethod
        def GetMessage(MessageId):
            # Makes the HTTP request
            response = client.get(Secure.baseurl+'/Message/'+MessageId, verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a MessageId string and displays the Mime string for that message
        @staticmethod
        def GetMimeMessage(MessageId):
            # Makes the HTTP request
            response = client.get(Secure.baseurl+'/Message/'+MessageId+'/Mime', verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a SendRequest Model and sends a message based on the give parameters
        @staticmethod
        def SendMessage(sendMessage = SendRequest()):
            # Creates a dictionary with the information from the model
            d={'To': sendMessage.To, 'Cc': sendMessage.Cc, 'Bcc': sendMessage.Bcc, 'Subject': sendMessage.Subject, 'Attachments': sendMessage.Attachments, 'HtmlBody': sendMessage.HtmlBody, 'TextBody': sendMessage.TextBody}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Message/', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a SendMimeRequest Model and sends a message based on the given Mime string
        @staticmethod
        def SendMimeMessage(sendMimeMessage = SendMimeRequest()):
            # Creates a dictionary with the information from the model
            d={'MimeMessage': sendMimeMessage.MimeMessage}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Message/Mime', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a MessageId string and a MoveRequest Model and moves the given message to a given folder
        @staticmethod
        def MoveMessage(MessageId, moveMessage = MoveRequest()):
            # Creates a dictionary with the information from the model
            d={'DestinationFolderId': moveMessage.DestinationFolderId}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Message/'+MessageId+'/Move', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                return(response.text)
            else:
                return(response.text)

        # Takes as input a MessageId string and deletes the given message
        @staticmethod
        def DeleteMessage(MessageId):
            # Makes the HTTP request
            response = client.delete(Secure.baseurl+'/Message/'+MessageId, verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a MessageId string and retracts the given message
        @staticmethod
        def RetractMessage(MessageId):
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Message/'+MessageId+'/Retract', data=None, verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                return(response.text)
            else:
                return(response.text)

        # Takes as input a MessageId string and displays the details without attachment data for that message
        @staticmethod
        def NoAttachmentData(MessageId):
            # Makes the HTTP request
            response = client.get(Secure.baseurl+'/Message/'+MessageId+'/NoAttachmentData', verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input an AttachmentId string and displays the details of that attachment
        @staticmethod
        def GetAttachment(AttachmentId):
            # Makes the HTTP request
            response = client.get(Secure.baseurl+'/Message/'+AttachmentId+'/Attachment', verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a SummariesWithMetaRequest Model 
        # and displays the summaries of the messages in a given folder with metadata
        @staticmethod
        def GetSummariesWithMeta(summsWithMeta = SummariesWithMetaRequest()):
            # Creates a dictionary with the information from the model
            d={'FolderId': summsWithMeta.FolderId, 'LastMessageIDReceived': summsWithMeta.LastMessageIDReceived}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Message/GetMessageSummariesWithMetadata', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a SaveDraftRequest Model and saves a draft of a message based on the given parameters
        @staticmethod
        def SaveDraft(saveDraft = SaveDraftRequest()):
            # Creates a dictionary with the information from the model
            d={'To': saveDraft.To, 'Cc': saveDraft.Cc, 'Bcc': saveDraft.Bcc, 'Subject': saveDraft.Subject, 'Attachments': saveDraft.Attachments, 'HtmlBody': saveDraft.HtmlBody, 'TextBody': saveDraft.TextBody}
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Message/SaveDraft', data= json.dumps(d), verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)

        # Takes as input a MessageId string and sends that drafted message
        @staticmethod
        def SendDraft(MessageId):
            # Makes the HTTP request
            response = client.post(Secure.baseurl+'/Message/'+MessageId+'/SendDraft', data=None, verify=True)
            # Ensures a successful status code
            if response.status_code == 200:
                # Formats the Response Body
                responseString = response.text
                res = json.loads(responseString)
                return(res)
            else:
                return(response.text)
