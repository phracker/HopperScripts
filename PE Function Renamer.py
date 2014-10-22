# Name: 
#    pe-func-renamer.py
# Version: 
#    0.1
# Description: 
#    This script will generically rename a function within Hopper, if the Windows PE binary contains certain Windows API 
#      names identified by Hopper as imports.       
# Author:
#    This is a "Hopper" port by Mick Grove (micksmix.wordpress.com) of Alexander Hanel's "func-renamer.py" script for IDA Pro.
#      *All* credit for the work behind this script goes to Alexander Hanel: alexander<dot>hanel<at>gmail<dot>com
#      Alexander's website is at: http://hooked-on-mnemonics.blogspot.com/
#
#

reg = [ 'Reg', 'RegCloseKey' ,'RegConnectRegistryA' ,'RegConnectRegistryW' ,'RegCreateKeyA' ,'RegCreateKeyExA' ,'RegCreateKeyExW',\
        'RegCreateKeyW' ,'RegDeleteKeyA' ,'RegDeleteKeyW' ,'RegDeleteValueA' ,'RegDeleteValueW' ,'RegDisablePredefinedCache' ,\
        'RegDisablePredefinedCacheEx' ,'RegEnumKeyA' ,'RegEnumKeyExA' ,'RegEnumKeyExW' ,'RegEnumKeyW' ,'RegEnumValueA' ,\
        'RegEnumValueW' ,'RegFlushKey' ,'RegGetKeySecurity' ,'RegLoadKeyA' ,'RegLoadKeyW' ,'RegNotifyChangeKeyValue' ,\
        'RegOpenCurrentUser' ,'RegOpenKeyA' ,'RegOpenKeyExA' ,'RegOpenKeyExW' ,'RegOpenKeyW' ,'RegOpenUserClassesRoot' ,\
        'RegOverridePredefKey' ,'RegQueryInfoKeyA' ,'RegQueryInfoKeyW' ,'RegQueryMultipleValuesA' ,'RegQueryMultipleValuesW' ,\
        'RegQueryValueA' ,'RegQueryValueExA' ,'RegQueryValueExW' ,'RegQueryValueW' ,'RegReplaceKeyA' ,'RegReplaceKeyW' ,\
        'RegRestoreKeyA' ,'RegRestoreKeyW' ,'RegSaveKeyA' ,'RegSaveKeyExA' ,'RegSaveKeyExW' ,'RegSaveKeyW' ,'RegSetKeySecurity' ,\
        'RegSetValueA' ,'RegSetValueExA' ,'RegSetValueExW' ,'RegSetValueW' ,'RegUnLoadKeyA' ,'RegUnLoadKeyW', 'SHDeleteEmptyKeyA' ,\
        'SHDeleteEmptyKeyW' ,'SHDeleteKeyA' ,'SHDeleteKeyW' ,'SHOpenRegStream2A' ,'SHOpenRegStream2W' ,'SHOpenRegStreamA' ,\
        'SHOpenRegStreamW' ,'SHQueryInfoKeyA' ,'SHQueryInfoKeyW' ,'SHQueryValueExA' ,'SHQueryValueExW' ,'SHRegCloseUSKey' ,\
        'SHRegCreateUSKeyA' ,'SHRegCreateUSKeyW' ,'SHRegDeleteEmptyUSKeyA' ,'SHRegDeleteEmptyUSKeyW' ,'SHRegDeleteUSValueA' ,\
        'SHRegDeleteUSValueW' ,'SHRegDuplicateHKey' ,'SHRegEnumUSKeyA' ,'SHRegEnumUSKeyW' ,'SHRegEnumUSValueA' ,'SHRegEnumUSValueW',\
        'SHRegGetBoolUSValueA' ,'SHRegGetBoolUSValueW' ,'SHRegGetPathA' ,'SHRegGetPathW' ,'SHRegGetUSValueA' ,'SHRegGetUSValueW' ,\
        'SHRegGetValueA' ,'SHRegGetValueW' ,'SHRegOpenUSKeyA' ,'SHRegOpenUSKeyW' ,'SHRegQueryInfoUSKeyA' ,'SHRegQueryInfoUSKeyW' ,\
        'SHRegQueryUSValueA' ,'SHRegQueryUSValueW' ,'SHRegSetPathA' ,'SHRegSetPathW' ,'SHRegSetUSValueA' ,'SHRegSetUSValueW' ,\
        'SHRegWriteUSValueA' ,'SHRegWriteUSValueW' ,'SHDeleteOrphanKeyA' ,'SHDeleteOrphanKeyW' ,'SHDeleteValueA' ,'SHDeleteValueW' ,\
        'SHEnumKeyExA' ,'SHEnumKeyExW' ,'SHEnumValueA' ,'SHEnumValueW' ,'SHGetValueA' ,'SHGetValueW' ,'SHOpenRegStream2A' ,\
        'SHOpenRegStream2W' ,'SHOpenRegStreamA' ,'SHOpenRegStreamW' ,'SHQueryInfoKeyA' ,'SHQueryInfoKeyW' ,'SHQueryValueExA' ,\
        'SHQueryValueExW' ,'SHRegCloseUSKey' ,'SHRegCreateUSKeyA' ,'SHRegCreateUSKeyW' ,'SHRegDeleteEmptyUSKeyA' ,\
        'SHRegDeleteEmptyUSKeyW' ,'SHRegDeleteUSValueA' ,'SHRegDeleteUSValueW' ,'SHRegDuplicateHKey' ,'SHRegEnumUSKeyA' ,\
        'SHRegEnumUSKeyW' ,'SHRegEnumUSValueA' ,'SHRegEnumUSValueW' ,'SHRegGetBoolUSValueA' ,'SHRegGetBoolUSValueW' ,'SHRegGetPathA' ,\
        'SHRegGetPathW' ,'SHRegGetUSValueA' ,'SHRegGetUSValueW' ,'SHRegGetValueA' ,'SHRegGetValueW' ,'SHRegOpenUSKeyA' ,'SHRegOpenUSKeyW' ,\
        'SHRegQueryInfoUSKeyA' ,'SHRegQueryInfoUSKeyW' ,'SHRegQueryUSValueA' ,'SHRegQueryUSValueW' ,'SHRegSetPathA' ,'SHRegSetPathW' ,\
        'SHRegSetUSValueA' ,'SHRegSetUSValueW' ,'SHRegWriteUSValueA' ,'SHRegWriteUSValueW']

# List of APIs related to socket
winsock = [ 'Ws2', 'FreeAddrInfoW', 'GetAddrInfoW', 'GetNameInfoW', 'WEP', 'WPUCompleteOverlappedRequest', 'WSAAccept', \
        'WSAAddressToStringA', 'WSAAddressToStringW', 'WSAAsyncGetHostByAddr', 'WSAAsyncGetHostByName', 'WSAAsyncGetProtoByName',\
        'WSAAsyncGetProtoByNumber', 'WSAAsyncGetServByName', 'WSAAsyncGetServByPort', 'WSAAsyncSelect', 'WSACancelAsyncRequest',\
        'WSACancelBlockingCall', 'WSACleanup', 'WSACloseEvent', 'WSAConnect', 'WSACreateEvent', 'WSADuplicateSocketA',\
        'WSADuplicateSocketW', 'WSAEnumNameSpaceProvidersA', 'WSAEnumNameSpaceProvidersW', 'WSAEnumNetworkEvents', 'WSAEnumProtocolsA',\
        'WSAEnumProtocolsW', 'WSAEventSelect', 'WSAGetLastError', 'WSAGetOverlappedResult', 'WSAGetQOSByName', \
        'WSAGetServiceClassInfoA', 'WSAGetServiceClassInfoW', 'WSAGetServiceClassNameByClassIdA', 'WSAGetServiceClassNameByClassIdW',\
        'WSAHtonl', 'WSAHtons', 'WSAInstallServiceClassA', 'WSAInstallServiceClassW', 'WSAIoctl', 'WSAIsBlocking', 'WSAJoinLeaf', \
        'WSALookupServiceBeginA', 'WSALookupServiceBeginW', 'WSALookupServiceEnd', 'WSALookupServiceNextA', 'WSALookupServiceNextW', \
        'WSANSPIoctl', 'WSANtohl', 'WSANtohs', 'WSAProviderConfigChange', 'WSARecv', 'WSARecvDisconnect', 'WSARecvFrom', \
        'WSARemoveServiceClass', 'WSAResetEvent', 'WSASend', 'WSASendDisconnect', 'WSASendTo', 'WSASetBlockingHook', 'WSASetEvent',\
        'WSASetLastError', 'WSASetServiceA', 'WSASetServiceW', 'WSASocketA', 'WSASocketW', 'WSAStartup', 'WSAStringToAddressA', \
        'WSAStringToAddressW', 'WSAUnhookBlockingHook', 'WSAWaitForMultipleEvents', 'WSApSetPostRoutine', 'WSCDeinstallProvider', \
        'WSCEnableNSProvider', 'WSCEnumProtocols', 'WSCGetProviderPath', 'WSCInstallNameSpace', 'WSCInstallProvider', 'WSCUnInstallNameSpace',\
        'WSCUpdateProvider', 'WSCWriteNameSpaceOrder', 'WSCWriteProviderOrder', '__WSAFDIsSet', 'accept', 'bind', 'closesocket', 'connect', \
        'freeaddrinfo', 'getaddrinfo', 'gethostbyaddr', 'gethostbyname', 'gethostname', 'getnameinfo', 'getpeername', 'getprotobyname', \
        'getprotobynumber', 'getservbyname', 'getservbyport', 'getsockname', 'getsockopt', 'htonl', 'htons', 'inet_addr', 'inet_ntoa', \
        'ioctlsocket', 'listen', 'ntohl', 'ntohs', 'recv', 'recvfrom', 'select', 'send', 'sendto', 'setsockopt', 'shutdown', 'socket']

WinINet = [ 'WINet', 'CreateMD5SSOHash', 'DetectAutoProxyUrl', 'DllInstall', 'ForceNexusLookup', 'ForceNexusLookupExW', 'InternetAlgIdToStringA',\
        'InternetAlgIdToStringW', 'InternetAttemptConnect', 'InternetAutodial', 'InternetAutodialCallback', 'InternetAutodialHangup',\
        'InternetCanonicalizeUrlA', 'InternetCanonicalizeUrlW', 'InternetCheckConnectionA', 'InternetCheckConnectionW', \
        'InternetClearAllPerSiteCookieDecisions', 'InternetCloseHandle', 'InternetCombineUrlA', 'InternetCombineUrlW', \
        'InternetConfirmZoneCrossing', 'InternetConfirmZoneCrossingA', 'InternetConfirmZoneCrossingW', 'InternetConnectA',\
        'InternetConnectW', 'InternetCrackUrlA', 'InternetCrackUrlW', 'InternetCreateUrlA', 'InternetCreateUrlW', 'InternetDial',\
        'InternetDialA', 'InternetDialW', 'InternetEnumPerSiteCookieDecisionA', 'InternetEnumPerSiteCookieDecisionW', 'InternetErrorDlg',\
        'InternetFindNextFileA', 'InternetFindNextFileW', 'InternetFortezzaCommand', 'InternetGetCertByURL', 'InternetGetCertByURLA',\
        'InternetGetConnectedState', 'InternetGetConnectedStateEx', 'InternetGetConnectedStateExA', 'InternetGetConnectedStateExW',\
        'InternetGetCookieA', 'InternetGetCookieExA', 'InternetGetCookieExW', 'InternetGetCookieW', 'InternetGetLastResponseInfoA', \
        'InternetGetLastResponseInfoW', 'InternetGetPerSiteCookieDecisionA', 'InternetGetPerSiteCookieDecisionW', 'InternetGoOnline',\
        'InternetGoOnlineA', 'InternetGoOnlineW', 'InternetHangUp', 'InternetInitializeAutoProxyDll', 'InternetLockRequestFile',\
        'InternetOpenA', 'InternetOpenUrlA', 'InternetOpenUrlW', 'InternetOpenW', 'InternetQueryDataAvailable', 'InternetQueryFortezzaStatus',\
        'InternetQueryOptionA', 'InternetQueryOptionW', 'InternetReadFile', 'InternetReadFileExA', 'InternetReadFileExW', \
        'InternetSecurityProtocolToStringA', 'InternetSecurityProtocolToStringW', 'InternetSetCookieA', 'InternetSetCookieExA', \
        'InternetSetCookieExW', 'InternetSetCookieW', 'InternetSetDialState', 'InternetSetDialStateA', 'InternetSetDialStateW',\
        'InternetSetFilePointer', 'InternetSetOptionA', 'InternetSetOptionExA', 'InternetSetOptionExW', 'InternetSetOptionW', \
        'InternetSetPerSiteCookieDecisionA', 'InternetSetPerSiteCookieDecisionW', 'InternetSetStatusCallback', 'InternetSetStatusCallbackA',\
        'InternetSetStatusCallbackW', 'InternetShowSecurityInfoByURL', 'InternetShowSecurityInfoByURLA', 'InternetShowSecurityInfoByURLW', \
        'InternetTimeFromSystemTime', 'InternetTimeFromSystemTimeA', 'InternetTimeFromSystemTimeW', 'InternetTimeToSystemTime',\
        'InternetTimeToSystemTimeA', 'InternetTimeToSystemTimeW', 'InternetUnlockRequestFile', 'InternetWriteFile', 'InternetWriteFileExA',\
        'InternetWriteFileExW', 'IsHostInProxyBypassList', 'ParseX509EncodedCertificateForListBoxEntry', 'PrivacyGetZonePreferenceW', \
        'PrivacySetZonePreferenceW', 'ResumeSuspendedDownload', 'ShowCertificate', 'ShowClientAuthCerts', 'ShowSecurityInfo', \
        'ShowX509EncodedCertificate','UrlZonesDetach', '_GetFileExtensionFromUrl']

cache = [ 'Cach','CommitUrlCacheEntryA', 'CommitUrlCacheEntryW', 'CreateUrlCacheContainerA', 'CreateUrlCacheContainerW', 'CreateUrlCacheEntryA',\
        'CreateUrlCacheEntryW', 'CreateUrlCacheGroup', 'DeleteIE3Cache', 'DeleteUrlCacheContainerA', 'DeleteUrlCacheContainerW', \
        'DeleteUrlCacheEntry', 'DeleteUrlCacheEntryA', 'DeleteUrlCacheEntryW', 'DeleteUrlCacheGroup', 'FindCloseUrlCache', 'FindFirstUrlCacheContainerA',\
        'FindFirstUrlCacheContainerW', 'FindFirstUrlCacheEntryA', 'FindFirstUrlCacheEntryExA', 'FindFirstUrlCacheEntryExW', 'FindFirstUrlCacheEntryW', \
        'FindFirstUrlCacheGroup', 'FindNextUrlCacheContainerA', 'FindNextUrlCacheContainerW', 'FindNextUrlCacheEntryA', 'FindNextUrlCacheEntryExA',\
        'FindNextUrlCacheEntryExW', 'FindNextUrlCacheEntryW', 'FindNextUrlCacheGroup', 'FreeUrlCacheSpaceA', 'FreeUrlCacheSpaceW', 'GetUrlCacheConfigInfoA', \
        'GetUrlCacheConfigInfoW', 'GetUrlCacheEntryInfoA', 'GetUrlCacheEntryInfoExA', 'GetUrlCacheEntryInfoExW', 'GetUrlCacheEntryInfoW', \
        'GetUrlCacheGroupAttributeA', 'GetUrlCacheGroupAttributeW', 'GetUrlCacheHeaderData', 'IncrementUrlCacheHeaderData', 'IsUrlCacheEntryExpiredA',\
        'IsUrlCacheEntryExpiredW', 'LoadUrlCacheContent', 'ReadUrlCacheEntryStream', 'RegisterUrlCacheNotification', 'RetrieveUrlCacheEntryFileA', \
        'RetrieveUrlCacheEntryFileW', 'RetrieveUrlCacheEntryStreamA', 'RetrieveUrlCacheEntryStreamW', 'RunOnceUrlCache', 'SetUrlCacheConfigInfoA',\
        'SetUrlCacheConfigInfoW', 'SetUrlCacheEntryGroup', 'SetUrlCacheEntryGroupA', 'SetUrlCacheEntryGroupW', 'SetUrlCacheEntryInfoA', 'SetUrlCacheEntryInfoW',\
        'SetUrlCacheGroupAttributeA', 'SetUrlCacheGroupAttributeW', 'SetUrlCacheHeaderData', 'UnlockUrlCacheEntryFile', 'UnlockUrlCacheEntryFileA', \
        'UnlockUrlCacheEntryFileW', 'UnlockUrlCacheEntryStream', 'UpdateUrlCacheContentPath']

ftp = [ 'Ftp','FtpCommandA' ,'FtpCommandW' ,'FtpCreateDirectoryA' ,'FtpCreateDirectoryW' ,'FtpDeleteFileA' ,'FtpDeleteFileW' ,'FtpFindFirstFileA' ,\
        'FtpFindFirstFileW' ,'FtpGetCurrentDirectoryA' ,'FtpGetCurrentDirectoryW' ,'FtpGetFileA' ,'FtpGetFileEx' ,'FtpGetFileSize' ,'FtpGetFileW' ,\
        'FtpOpenFileA' ,'FtpOpenFileW' ,'FtpPutFileA' ,'FtpPutFileEx' ,'FtpPutFileW' ,'FtpRemoveDirectoryA' ,'FtpRemoveDirectoryW' ,'FtpRenameFileA' ,\
        'FtpRenameFileW' ,'FtpSetCurrentDirectoryA' ,'FtpSetCurrentDirectoryW']

gopher = [ 'Gopher', 'GopherCreateLocatorA', 'GopherCreateLocatorW', 'GopherFindFirstFileA', 'GopherFindFirstFileW', 'GopherGetAttributeA', \
		   'GopherGetAttributeW', 'GopherGetLocatorTypeA', 'GopherGetLocatorTypeW', 'GopherOpenFileA', 'GopherOpenFileW'] 

# Shlwapi.dll
url = ['Url', 'UrlApplySchemeA' ,'UrlApplySchemeW' ,'UrlCanonicalizeA' ,'UrlCanonicalizeW' ,'UrlCombineA' ,'UrlCombineW' ,'UrlCompareA' ,\
	   'UrlCompareW' ,'UrlCreateFromPathA' ,'UrlCreateFromPathW' ,'UrlEscapeA' ,'UrlEscapeW' ,'UrlGetLocationA' ,'UrlGetLocationW' ,'UrlGetPartA'\
	   ,'UrlGetPartW' ,'UrlHashA' ,'UrlHashW' ,'UrlIsA' ,'UrlIsNoHistoryA' ,'UrlIsNoHistoryW' ,'UrlIsOpaqueA' ,'UrlIsOpaqueW' ,'UrlIsW' ,'UrlUnescapeA' ,'UrlUnescapeW']

dir = ['Dir','CreateDirectoryA', 'CreateDirectoryExA', 'CreateDirectoryExW', 'CreateDirectoryW', 'GetCurrentDirectoryA', 'GetCurrentDirectoryW',\
	   'GetDllDirectoryA', 'GetDllDirectoryW', 'GetSystemDirectoryA', 'GetSystemDirectoryW', 'GetSystemWindowsDirectoryA', 'GetSystemWindowsDirectoryW',\
	   'GetSystemWow64DirectoryA', 'GetSystemWow64DirectoryW', 'GetVDMCurrentDirectories', 'GetWindowsDirectoryA', 'GetWindowsDirectoryW', \
	   'ReadDirectoryChangesW', 'RemoveDirectoryA', 'RemoveDirectoryW', 'SetCurrentDirectoryA', 'SetCurrentDirectoryW', 'SetDllDirectoryA',\
	   'SetDllDirectoryW', 'SetVDMCurrentDirectories', 'SHCreateDirectory', 'SHCreateDirectoryExA', 'SHCreateDirectoryExW']

# Mutex
mutex = ['Mutx','CreateMutexA', 'CreateMutexW', 'OpenMutexA', 'OpenMutexW', 'ReleaseMutex']

# Pipe 
pipe = [ 'Pipe', 'CallNamedPipeA', 'CallNamedPipeW', 'ConnectNamedPipe', 'CreateNamedPipeA', 'CreateNamedPipeW', 'CreatePipe', 'DisconnectNamedPipe',\
		 'GetNamedPipeHandleStateA', 'GetNamedPipeHandleStateW', 'GetNamedPipeInfo', 'PeekNamedPipe', 'SetNamedPipeHandleState', 'TransactNamedPipe',\
		 'WaitNamedPipeA', 'WaitNamedPipeW']

# List of APIs related to HTTP from WinINet
http = [ 'Http', 'HttpAddRequestHeadersA', 'HttpAddRequestHeadersW', 'HttpCheckDavCompliance', 'HttpEndRequestA', 'HttpEndRequestW',\
		 'HttpOpenRequestA', 'HttpOpenRequestW', 'HttpQueryInfoA', 'HttpQueryInfoW', 'HttpSendRequestA', 'HttpSendRequestExA', \
		 'HttpSendRequestExW', 'HttpSendRequestW' ] 

# enum process
enum = [ 'Enum', 'CreateToolhelp32Snapshot', 'Process32First' ,'Process32FirstW' ,'Process32Next' ,'Process32NextW']

# List of APIs related to hashing files
hash = ['Hash', 'CryptCreateHash' ,'CryptDestroyHash' ,'CryptDuplicateHash' ,'CryptGetHashParam' ,'CryptHashData' ,'CryptHashSessionKey' ,\
		'CryptSetHashParam' ,'CryptSignHashA' ,'CryptSignHashW', 'FreeEncryptionCertificateHashList']

# List of APIs related to Cryptography files
crypt = ['Crypt', 'CryptAcquireContextA' ,'CryptAcquireContextW' ,'CryptContextAddRef' ,'CryptDecrypt' ,'CryptDeriveKey' ,'CryptDestroyKey' ,\
        'CryptDuplicateKey' ,'CryptEncrypt' ,'CryptEnumProviderTypesA' ,'CryptEnumProviderTypesW' ,'CryptEnumProvidersA' ,'CryptEnumProvidersW'\
        ,'CryptExportKey' ,'CryptGenKey' ,'CryptGenRandom' ,'CryptGetDefaultProviderA' ,'CryptGetDefaultProviderW' ,'CryptGetKeyParam' ,\
        'CryptGetProvParam' ,'CryptGetUserKey' ,'CryptImportKey' ,'CryptReleaseContext' ,'CryptSetKeyParam' ,'CryptSetProvParam' ,\
        'CryptSetProviderA' ,'CryptSetProviderExA' ,'CryptSetProviderExW' ,'CryptSetProviderW' ,'CryptVerifySignatureA' ,'CryptVerifySignatureW' ,\
        'DecryptFileA' ,'DecryptFileW', 'EncryptFileA' ,'EncryptFileW' ,'EncryptedFileKeyInfo' ,'EncryptionDisable', 'WriteEncryptedFileRaw', \
        'OpenEncryptedFileRawA' ,'OpenEncryptedFileRawW', 'DuplicateEncryptionInfoFile', 'SetUserFileEncryptionKey', 'ReadEncryptedFileRaw', \
        'RemoveUsersFromEncryptedFile', 'FileEncryptionStatusA', 'FileEncryptionStatusW', 'FreeEncryptedFileKeyInfo', 'CloseEncryptedFileRaw', \
        'AddUsersToEncryptedFile', 'QueryRecoveryAgentsOnEncryptedFile', 'QueryUsersOnEncryptedFile', 'ChainWlxLogoffEvent' ,'CryptAcquireContextU' ,\
        'CryptBinaryToStringA' ,'CryptBinaryToStringW' ,'CryptCloseAsyncHandle' ,'CryptCreateAsyncHandle' ,'CryptDecodeMessage' ,'CryptDecodeObject' ,\
        'CryptDecodeObjectEx' ,'CryptDecryptAndVerifyMessageSignature' ,'CryptDecryptMessage' ,'CryptEncodeObject' ,'CryptEncodeObjectEx' ,\
        'CryptEncryptMessage' ,'CryptEnumKeyIdentifierProperties' ,'CryptEnumOIDFunction' ,'CryptEnumOIDInfo' ,'CryptEnumProvidersU' ,'CryptExportPKCS8' ,\
        'CryptExportPublicKeyInfo' ,'CryptExportPublicKeyInfoEx' ,'CryptFindLocalizedName' ,'CryptFindOIDInfo' ,'CryptFormatObject' ,\
        'CryptFreeOIDFunctionAddress' ,'CryptGetAsyncParam' ,'CryptGetDefaultOIDDllList' ,'CryptGetDefaultOIDFunctionAddress' ,\
        'CryptGetKeyIdentifierProperty' ,'CryptGetMessageCertificates' ,'CryptGetMessageSignerCount' ,'CryptGetOIDFunctionAddress' ,\
        'CryptGetOIDFunctionValue' ,'CryptHashCertificate' ,'CryptHashMessage' ,'CryptHashPublicKeyInfo' ,'CryptHashToBeSigned' ,\
        'CryptImportPKCS8' ,'CryptImportPublicKeyInfo' ,'CryptImportPublicKeyInfoEx' ,'CryptInitOIDFunctionSet' ,'CryptInstallDefaultContext' ,\
        'CryptInstallOIDFunctionAddress' ,'CryptLoadSip' ,'CryptMemAlloc' ,'CryptMemFree' ,'CryptMemRealloc' ,'CryptMsgCalculateEncodedLength' ,\
        'CryptMsgClose' ,'CryptMsgControl' ,'CryptMsgCountersign' ,'CryptMsgCountersignEncoded' ,'CryptMsgDuplicate' ,'CryptMsgEncodeAndSignCTL' ,\
        'CryptMsgGetAndVerifySigner' ,'CryptMsgGetParam' ,'CryptMsgOpenToDecode' ,'CryptMsgOpenToEncode' ,'CryptMsgSignCTL' ,'CryptMsgUpdate' ,\
        'CryptMsgVerifyCountersignatureEncoded' ,'CryptMsgVerifyCountersignatureEncodedEx' ,'CryptProtectData' ,'CryptQueryObject' ,\
        'CryptRegisterDefaultOIDFunction' ,'CryptRegisterOIDFunction' ,'CryptRegisterOIDInfo' ,'CryptSIPAddProvider' ,\
        'CryptSIPCreateIndirectData' ,'CryptSIPGetSignedDataMsg' ,'CryptSIPLoad' ,'CryptSIPPutSignedDataMsg' ,'CryptSIPRemoveProvider' ,\
        'CryptSIPRemoveSignedDataMsg' ,'CryptSIPRetrieveSubjectGuid' ,'CryptSIPRetrieveSubjectGuidForCatalogFile' ,'CryptSIPVerifyIndirectData' ,\
        'CryptSetAsyncParam' ,'CryptSetKeyIdentifierProperty' ,'CryptSetOIDFunctionValue' ,'CryptSetProviderU' ,'CryptSignAndEncodeCertificate' ,\
        'CryptSignAndEncryptMessage' ,'CryptSignCertificate' ,'CryptSignHashU' ,'CryptSignMessage' ,'CryptSignMessageWithKey' ,\
        'CryptStringToBinaryA' ,'CryptStringToBinaryW' ,'CryptUninstallDefaultContext' ,'CryptUnprotectData' ,'CryptUnregisterDefaultOIDFunction' ,\
        'CryptUnregisterOIDFunction' ,'CryptUnregisterOIDInfo' ,'CryptVerifyCertificateSignature' ,'CryptVerifyCertificateSignatureEx' ,\
        'CryptVerifyDetachedMessageHash' ,'CryptVerifyDetachedMessageSignature' ,'CryptVerifyMessageHash' ,'CryptVerifyMessageSignature' ,\
        'CryptVerifyMessageSignatureWithKey' ,'CryptVerifySignatureU' ,'I_CertProtectFunction' ,'I_CertSrvProtectFunction' ,'I_CertSyncStore' ,\
        'I_CertUpdateStore' ,'I_CryptAddRefLruEntry' ,'I_CryptAddSmartCardCertToStore' ,'I_CryptAllocTls' ,'I_CryptCreateLruCache' ,\
        'I_CryptCreateLruEntry' ,'I_CryptDetachTls' ,'I_CryptDisableLruOfEntries' ,'I_CryptEnableLruOfEntries' ,'I_CryptEnumMatchingLruEntries' ,\
        'I_CryptFindLruEntry' ,'I_CryptFindLruEntryData' ,'I_CryptFindSmartCardCertInStore' ,'I_CryptFlushLruCache' ,'I_CryptFreeLruCache' ,\
        'I_CryptFreeTls' ,'I_CryptGetAsn1Decoder' ,'I_CryptGetAsn1Encoder' ,'I_CryptGetDefaultCryptProv' ,'I_CryptGetDefaultCryptProvForEncrypt' ,\
        'I_CryptGetFileVersion' ,'I_CryptGetLruEntryData' ,'I_CryptGetLruEntryIdentifier' ,'I_CryptGetOssGlobal' ,'I_CryptGetTls' ,'I_CryptInsertLruEntry' ,\
        'I_CryptInstallAsn1Module' ,'I_CryptInstallOssGlobal' ,'I_CryptReadTrustedPublisherDWORDValueFromRegistry' ,'I_CryptRegisterSmartCardStore' ,\
        'I_CryptReleaseLruEntry' ,'I_CryptRemoveLruEntry' ,'I_CryptSetTls' ,'I_CryptTouchLruEntry' ,'I_CryptUninstallAsn1Module' ,\
        'I_CryptUninstallOssGlobal' ,'I_CryptUnregisterSmartCardStore' ,'I_CryptWalkAllLruCacheEntries']

service = ['Serv', 'ChangeServiceConfig2A' ,'ChangeServiceConfig2W' ,'ChangeServiceConfigA' ,'ChangeServiceConfigW' ,'CloseServiceHandle' ,\
        'ControlService' ,'CreateServiceA' ,'CreateServiceW' ,'DeleteService' ,'EnumDependentServicesA' ,'EnumDependentServicesW' ,\
        'EnumServiceGroupW' ,'EnumServicesStatusA' ,'EnumServicesStatusExA' ,'EnumServicesStatusExW' ,'EnumServicesStatusW' ,\
        'GetServiceDisplayNameA' ,'GetServiceDisplayNameW' ,'GetServiceKeyNameA' ,'GetServiceKeyNameW' ,'I_ScPnPGetServiceName' ,\
        'I_ScSetServiceBitsA' ,'I_ScSetServiceBitsW' ,'LockServiceDatabase' ,'OpenServiceA' ,'OpenServiceW' ,'PrivilegedServiceAuditAlarmA' ,\
        'PrivilegedServiceAuditAlarmW' ,'QueryServiceConfig2A' ,'QueryServiceConfig2W' ,'QueryServiceConfigA' ,'QueryServiceConfigW' ,\
        'QueryServiceLockStatusA' ,'QueryServiceLockStatusW' ,'QueryServiceObjectSecurity' ,'QueryServiceStatus' ,'QueryServiceStatusEx' ,\
        'RegisterServiceCtrlHandlerA' ,'RegisterServiceCtrlHandlerExA' ,'RegisterServiceCtrlHandlerExW' ,'RegisterServiceCtrlHandlerW' ,\
        'SetServiceBits' ,'SetServiceObjectSecurity' ,'SetServiceStatus' ,'StartServiceA' ,'StartServiceCtrlDispatcherA' ,'StartServiceCtrlDispatcherW' ,\
        'StartServiceW' ,'UnlockServiceDatabase' ,'WdmWmiServiceMain']

# Generic File Operations 
file = ['File', 'CompareFileTime' ,'CopyFileA' ,'CopyFileExA' ,'CopyFileExW' ,'CopyFileW' ,'CopyLZFile' ,'CreateFileA' ,'CreateFileMappingA' ,\
        'CreateFileMappingW' ,'CreateFileW' ,'DeleteFileA' ,'DeleteFileW' ,'DosDateTimeToFileTime' ,'FileTimeToDosDateTime' ,\
        'FileTimeToLocalFileTime' ,'FileTimeToLocalFileTime' ,'FileTimeToSystemTime' ,'FlushFileBuffers' ,'FlushViewOfFile' ,\
        'GetCPFileNameFromRegistry' ,'GetCompressedFileSizeA' ,'GetCompressedFileSizeW' ,'GetFileAttributesA' ,'GetFileAttributesExA' ,\
        'GetFileAttributesExW' ,'GetFileAttributesW' ,'GetFileInformationByHandle' ,'GetFileSize' ,'GetFileSizeEx' ,'GetFileTime' ,\
        'GetFileType' ,'GetSystemTimeAsFileTime' ,'GetTempFileNameA' ,'GetTempFileNameW' ,'LZCloseFile' ,'LZCreateFileW' ,'LZOpenFileA',\
        'LZOpenFileW' ,'LocalFileTimeToFileTime' ,'LocalFileTimeToFileTime' ,'LockFile' ,'LockFileEx' ,'MapViewOfFile' ,'MapViewOfFileEx' ,\
        'MoveFileA' ,'MoveFileExA' ,'MoveFileExW' ,'MoveFileW' ,'MoveFileWithProgressA' ,'MoveFileWithProgressW' ,'OpenDataFile' ,'OpenFile' ,\
        'OpenFileMappingA' ,'OpenFileMappingW' ,'OpenProfileUserMapping' ,'PrivCopyFileExW' ,'PrivMoveFileIdentityW' ,'ReadFile' ,'ReadFileEx' ,\
        'ReplaceFile' ,'ReplaceFileA' ,'ReplaceFileW' ,'SetEndOfFile' ,'SetFileAttributesA' ,'SetFileAttributesW' ,'SetFilePointer' ,\
        'SetFilePointerEx' ,'SetFileShortNameA' ,'SetFileShortNameW' ,'SetFileTime' ,'SetFileValidData' ,'SystemTimeToFileTime' ,\
        'UnlockFile' ,'UnlockFileEx' ,'UnmapViewOfFile' ,'WriteFile' ,'WriteFileEx' ,'WriteFileGather' ,'GetFileSecurityA' ,\
        'GetFileSecurityW' ,'SetFileSecurityA' ,'SetFileSecurityW', 'CreateFileU']

# APIs related to Collecting information about the host OS 
os_info = [ 'Info', 'GetComputerNameA' ,'GetComputerNameExA' ,'GetComputerNameExW' ,'GetComputerNameW' ,'GetDiskFreeSpaceA' ,\
			'GetDiskFreeSpaceExA' ,'GetDiskFreeSpaceExW' ,'GetDiskFreeSpaceW' ,'GetDriveTypeA' ,'GetDriveTypeW', 'GetVersion' ,\
			'GetVersionExA' ,'GetVersionExW', 'GetSystemInfo', 'GetSystemMetrics', 'CheckTokenMembership']

# List of APIs related to hashing files
cert = ['Cert','CertAddCRLContextToStore' ,'CertAddCRLLinkToStore' ,'CertAddCTLContextToStore' ,'CertAddCTLLinkToStore' ,\
		'CertAddCertificateContextToStore' ,'CertAddCertificateLinkToStore' ,'CertAddEncodedCRLToStore' ,'CertAddEncodedCertificateToStore' ,\
		'CertAddEncodedCertificateToSystemStoreA' ,'CertAddEncodedCertificateToSystemStoreW' ,'CertAddEnhancedKeyUsageIdentifier' ,\
		'CertAddSerializedElementToStore' ,'CertAddStoreToCollection' ,'CertAlgIdToOID' ,'CertCloseStore' ,'CertCompareCertificate' ,\
		'CertCompareCertificateName' ,'CertCompareIntegerBlob' ,'CertComparePublicKeyInfo' ,'CertControlStore' ,'CertCreateCTLContext' ,\
		'CertCreateCTLEntryFromCertificateContextProperties' ,'CertCreateCertificateChainEngine' ,'CertCreateCertificateContext' ,'CertCreateContext',\
		'CertCreateSelfSignCertificate' ,'CertDeleteCTLFromStore' ,'CertDeleteCertificateFromStore' ,'CertDuplicateCTLContext' ,\
		'CertDuplicateCertificateChain' ,'CertDuplicateCertificateContext' ,'CertDuplicateStore' ,'CertEnumCRLContextProperties' ,\
		'CertEnumCRLsInStore' ,'CertEnumCTLContextProperties' ,'CertEnumCTLsInStore' ,'CertEnumCertificateContextProperties' ,\
		'CertEnumCertificatesInStore' ,'CertEnumPhysicalStore' ,'CertEnumSubjectInSortedCTL' ,'CertEnumSystemStore' ,\
		'CertEnumSystemStoreLocation' ,'CertFindAttribute' ,'CertFindCRLInStore' ,'CertFindCertificateInCRL' ,'CertFindCertificateInStore',\
		'CertFindChainInStore' ,'CertFindExtension' ,'CertFindRDNAttr' ,'CertFindSubjectInCTL' ,'CertFindSubjectInSortedCTL' ,\
		'CertFreeCRLContext' ,'CertFreeCertificateChain' ,'CertFreeCertificateChainEngine' ,'CertFreeCertificateContext' ,'CertGetCRLContextProperty' ,\
		'CertGetCRLFromStore' ,'CertGetCTLContextProperty' ,'CertGetCertificateChain' ,'CertGetCertificateContextProperty' ,'CertGetEnhancedKeyUsage' ,\
		'CertGetIssuerCertificateFromStore' ,'CertGetNameStringA' ,'CertGetNameStringW' ,'CertGetPublicKeyLength' ,'CertGetStoreProperty' ,\
		'CertGetSubjectCertificateFromStore' ,'CertGetValidUsages' ,'CertIsRDNAttrsInCertificateName' ,'CertIsValidCRLForCertificate' ,\
		'CertNameToStrA' ,'CertNameToStrW' ,'CertOIDToAlgId' ,'CertOpenStore' ,'CertOpenSystemStoreA' ,'CertOpenSystemStoreW' ,'CertRDNValueToStrA',\
		'CertRDNValueToStrW' ,'CertRegisterPhysicalStore' ,'CertRegisterSystemStore' ,'CertRemoveEnhancedKeyUsageIdentifier' ,\
		'CertRemoveStoreFromCollection' ,'CertResyncCertificateChainEngine' ,'CertSaveStore' ,'CertSerializeCRLStoreElement' ,\
		'CertSerializeCertificateStoreElement' ,'CertSetCRLContextProperty' ,'CertSetCertificateContextPropertiesFromCTLEntry' ,\
		'CertSetCertificateContextProperty' ,'CertSetEnhancedKeyUsage' ,'CertSetStoreProperty' ,'CertStrToNameA' ,'CertStrToNameW' ,\
		'CertUnregisterPhysicalStore' ,'CertUnregisterSystemStore' ,'CertVerifyCRLRevocation' ,'CertVerifyCRLTimeValidity' ,\
		'CertVerifyCTLUsage' ,'CertVerifyCertificateChainPolicy' ,'CertVerifyCertificateChainPolicy' ,'CertVerifyRevocation' ,\
		'CertVerifySubjectCertificateContext','CertVerifyTimeValidity' ,'CertVerifyValidityNesting' ,'CloseCertPerformanceData' ,\
		'CollectCertPerformanceData' ,'CryptAcquireCertificatePrivateKey' ,'CryptFindCertificateKeyProvInfo' ,'CryptGetMessageCertificates' ,\
		'CryptHashCertificate' ,'CryptSignAndEncodeCertificate' ,'CryptSignCertificate' ,'CryptVerifyCertificateSignature' ,\
		'CryptVerifyCertificateSignatureEx' ,'I_CertProtectFunction' ,'I_CertSrvProtectFunction' ,'I_CertSyncStore' ,'I_CertUpdateStore' ,\
		'I_CryptAddSmartCardCertToStore' ,'I_CryptFindSmartCardCertInStore' ,'OpenCertPerformanceData' ,'PFXExportCertStore' ,'PFXExportCertStoreEx' ,'PFXImportCertStore'] 

# APIs related to searching 
file_s = ['FSear', 'FindFirstFileW', 'FindNextFileW', 'FindClose']

# Possible Hook or Injection functions
modify = ['Mod', 'WriteProcessMemory', 'ReadProcessMemory'] 

virtual = ['Virt', 'VirtualAlloc' ,'VirtualAllocEx' ,'VirtualBufferExceptionHandler' ,'VirtualFree' ,'VirtualFreeEx' ,'VirtualLock' ,
		   'VirtualProtect' ,'VirtualProtectEx' ,'VirtualQuery' ,'VirtualQueryEx' ,'VirtualUnlock']

critical_section = [ 'CrSec', 'DeleteCriticalSection' ,'EnterCriticalSection' ,'InitializeCriticalSection' ,
					 'InitializeCriticalSectionAndSpinCount' ,'LeaveCriticalSection' ,'SetCriticalSectionSpinCount' ,'TryEnterCriticalSection']

#the list are appended to make a matrix. Removes the problem of tracking each list of apis names in the code. Hopefully makes it easier to update. 
api_matrix = [ reg, winsock, WinINet, cache, ftp, gopher, dir, mutex, pipe, http, enum, hash, crypt, service, file, cert, os_info, file_s, modify, virtual, critical_section ]


doc = Document.getCurrentDocument()

for api_row in api_matrix:
	sApiCategory = api_row[0]
	apis = api_row[1:]
	for api in apis:
		curAddr = doc.getAddressForName("imp_" + api)

		if curAddr > 0:
			addrname = doc.getNameAtAddress(curAddr)
			print '  [+] %s' % (api)

			segmentApiImport = doc.getSegmentAtAddress(curAddr)
			refAddrs = segmentApiImport.getReferencesOfAddress(curAddr)
			
			for curRef in refAddrs:
				segCurRef = doc.getSegmentAtAddress(curRef)
				prIndex = segCurRef.getProcedureIndexAtAddress(curRef)
				
				if prIndex > 0:
					curPr = segCurRef.getProcedureAtIndex(prIndex)
					curPrEntry = curPr.getEntryPoint()
					curPrName = doc.getNameAtAddress(curPrEntry)
					if curPrName != None and curPrName.find(sApiCategory) == -1 :
						doc.setNameAtAddress(curPrEntry,sApiCategory + '_' + curPrName)
						print '     - %s_%s' % (sApiCategory,curPrName)
				
doc.refreshView()
print "[*] pe-func-renamer complete"
