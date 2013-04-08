doc = Document.getCurrentDocument()

doc.log("# WS2_32.dll ordinals to names v1.0")
doc.log("# Author: @chort0")
doc.log("# Greetz: @abad1dea @bsr43")
doc.log("# Ord => Name mapping from http://www.winasm.net/forum/index.php?showtopic=2362")

ordinals = {'imp_ordinal_1' : 'imp_accept',
'imp_ordinal_2' : 'imp_bind',
'imp_ordinal_3' : 'imp_closesocket',
'imp_ordinal_4' : 'imp_connect',
'imp_ordinal_5' : 'imp_getpeername',
'imp_ordinal_6' : 'imp_getsockname',
'imp_ordinal_7' : 'imp_getsockopt',
'imp_ordinal_8' : 'imp_htonl',
'imp_ordinal_9' : 'imp_htons',
'imp_ordinal_10' : 'imp_ioctlsocket',
'imp_ordinal_11' : 'imp_inet_addr',
'imp_ordinal_12' : 'imp_inet_ntoa',
'imp_ordinal_13' : 'imp_listen',
'imp_ordinal_14' : 'imp_ntohl',
'imp_ordinal_15' : 'imp_ntohs',
'imp_ordinal_16' : 'imp_recv',
'imp_ordinal_17' : 'imp_recvfrom',
'imp_ordinal_18' : 'imp_select',
'imp_ordinal_19' : 'imp_send',
'imp_ordinal_20' : 'imp_sendto',
'imp_ordinal_21' : 'imp_setsockopt',
'imp_ordinal_22' : 'imp_shutdown',
'imp_ordinal_23' : 'imp_socket',
'imp_ordinal_24' : 'imp_GetAddrInfoW',
'imp_ordinal_25' : 'imp_GetNameInfoW',
'imp_ordinal_26' : 'imp_WSApSetPostRoutine',
'imp_ordinal_27' : 'imp_FreeAddrInfoW',
'imp_ordinal_28' : 'imp_WPUCompleteOverlappedRequest',
'imp_ordinal_29' : 'imp_WSAAccept',
'imp_ordinal_30' : 'imp_WSAAddressToStringA',
'imp_ordinal_31' : 'imp_WSAAddressToStringW',
'imp_ordinal_32' : 'imp_WSACloseEvent',
'imp_ordinal_33' : 'imp_WSAConnect',
'imp_ordinal_34' : 'imp_WSACreateEvent',
'imp_ordinal_35' : 'imp_WSADuplicateSocketA',
'imp_ordinal_36' : 'imp_WSADuplicateSocketW',
'imp_ordinal_37' : 'imp_WSAEnumNameSpaceProvidersA',
'imp_ordinal_38' : 'imp_WSAEnumNameSpaceProvidersW',
'imp_ordinal_39' : 'imp_WSAEnumNetworkEvents',
'imp_ordinal_40' : 'imp_WSAEnumProtocolsA',
'imp_ordinal_41' : 'imp_WSAEnumProtocolsW',
'imp_ordinal_42' : 'imp_WSAEventSelect',
'imp_ordinal_43' : 'imp_WSAGetOverlappedResult',
'imp_ordinal_44' : 'imp_WSAGetQOSByName',
'imp_ordinal_45' : 'imp_WSAGetServiceClassInfoA',
'imp_ordinal_46' : 'imp_WSAGetServiceClassInfoW',
'imp_ordinal_47' : 'imp_WSAGetServiceClassNameByClassIdA',
'imp_ordinal_48' : 'imp_WSAGetServiceClassNameByClassIdW',
'imp_ordinal_49' : 'imp_WSAHtonl',
'imp_ordinal_50' : 'imp_WSAHtons',
'imp_ordinal_51' : 'imp_gethostbyaddr',
'imp_ordinal_52' : 'imp_gethostbyname',
'imp_ordinal_53' : 'imp_getprotobyname',
'imp_ordinal_54' : 'imp_getprotobynumber',
'imp_ordinal_55' : 'imp_getservbyname',
'imp_ordinal_56' : 'imp_getservbyport',
'imp_ordinal_57' : 'imp_gethostname',
'imp_ordinal_58' : 'imp_WSAInstallServiceClassA',
'imp_ordinal_59' : 'imp_WSAInstallServiceClassW',
'imp_ordinal_60' : 'imp_WSAIoctl',
'imp_ordinal_61' : 'imp_WSAJoinLeaf',
'imp_ordinal_62' : 'imp_WSALookupServiceBeginA',
'imp_ordinal_63' : 'imp_WSALookupServiceBeginW',
'imp_ordinal_64' : 'imp_WSALookupServiceEnd',
'imp_ordinal_65' : 'imp_WSALookupServiceNextA',
'imp_ordinal_66' : 'imp_WSALookupServiceNextW',
'imp_ordinal_67' : 'imp_WSANSPIoctl',
'imp_ordinal_68' : 'imp_WSANtohl',
'imp_ordinal_69' : 'imp_WSANtohs',
'imp_ordinal_70' : 'imp_WSAProviderConfigChange',
'imp_ordinal_71' : 'imp_WSARecv',
'imp_ordinal_72' : 'imp_WSARecvDisconnect',
'imp_ordinal_73' : 'imp_WSARecvFrom',
'imp_ordinal_74' : 'imp_WSARemoveServiceClass',
'imp_ordinal_75' : 'imp_WSAResetEvent',
'imp_ordinal_76' : 'imp_WSASend',
'imp_ordinal_77' : 'imp_WSASendDisconnect',
'imp_ordinal_78' : 'imp_WSASendTo',
'imp_ordinal_79' : 'imp_WSASetEvent',
'imp_ordinal_80' : 'imp_WSASetServiceA',
'imp_ordinal_81' : 'imp_WSASetServiceW',
'imp_ordinal_82' : 'imp_WSASocketA',
'imp_ordinal_83' : 'imp_WSASocketW',
'imp_ordinal_84' : 'imp_WSAStringToAddressA',
'imp_ordinal_85' : 'imp_WSAStringToAddressW',
'imp_ordinal_86' : 'imp_WSAWaitForMultipleEvents',
'imp_ordinal_87' : 'imp_WSCDeinstallProvider',
'imp_ordinal_88' : 'imp_WSCEnableNSProvider',
'imp_ordinal_89' : 'imp_WSCEnumProtocols',
'imp_ordinal_90' : 'imp_WSCGetProviderPath',
'imp_ordinal_91' : 'imp_WSCInstallNameSpace',
'imp_ordinal_92' : 'imp_WSCInstallProvider',
'imp_ordinal_93' : 'imp_WSCUnInstallNameSpace',
'imp_ordinal_94' : 'imp_WSCUpdateProvider',
'imp_ordinal_95' : 'imp_WSCWriteNameSpaceOrder',
'imp_ordinal_96' : 'imp_WSCWriteProviderOrder',
'imp_ordinal_97' : 'imp_freeaddrinfo',
'imp_ordinal_98' : 'imp_getaddrinfo',
'imp_ordinal_99' : 'imp_getnameinfo',
'imp_ordinal_101' : 'imp_WSAAsyncSelect',
'imp_ordinal_102' : 'imp_WSAAsyncGetHostByAddr',
'imp_ordinal_103' : 'imp_WSAAsyncGetHostByName',
'imp_ordinal_104' : 'imp_WSAAsyncGetProtoByNumber',
'imp_ordinal_105' : 'imp_WSAAsyncGetProtoByName',
'imp_ordinal_106' : 'imp_WSAAsyncGetServByPort',
'imp_ordinal_107' : 'imp_WSAAsyncGetServByName',
'imp_ordinal_108' : 'imp_WSACancelAsyncRequest',
'imp_ordinal_109' : 'imp_WSASetBlockingHook',
'imp_ordinal_110' : 'imp_WSAUnhookBlockingHook',
'imp_ordinal_111' : 'imp_WSAGetLastError',
'imp_ordinal_112' : 'imp_WSASetLastError',
'imp_ordinal_113' : 'imp_WSACancelBlockingCall',
'imp_ordinal_114' : 'imp_WSAIsBlocking',
'imp_ordinal_115' : 'imp_WSAStartup',
'imp_ordinal_116' : 'imp_WSACleanup',
'imp_ordinal_151' : 'imp___WSAFDIsSet',
'imp_ordinal_500' : 'imp_WEP'
}
theRange = doc.getSelectionAddressRange()
lower = theRange[0]
upper = theRange[1]

doc.log("Renaming in range %s to %s" % (hex(lower), hex(upper)))

adr = lower
while adr <= upper:
	doc.log("Address: %d" % adr)
	name = doc.getNameAtAddress(adr)
	if name != None:
		doc.log("Name: %s" % name)
		newName = ordinals[name]
		if newName != None:
			doc.log("Renaming %s to %s" % (name, newName))
			doc.setNameAtAddress(adr, newName)
	adr = adr + 4
	name = ''
doc.log("# end of script")
doc.refreshView()