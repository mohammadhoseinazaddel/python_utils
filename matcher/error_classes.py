import ErrorCodes
import logging
import traceback

logger = logging.getLogger('ui.error_classes')


class SabError(Exception):
    def __init__(self, msg, error_code, interface_err=None):
        self.msg = msg
        self.error_code = error_code
        self.interface_err = interface_err
        # log debug message that contains traceback
        log_message = 'Input Parameters: message="%s" error_code="%i" Interface_error="%s"\n' % \
                      (self.msg, self.error_code, interface_err)
        for item in traceback.format_stack():
            log_message += item
        # logger.debug(log_message) TODO: Enable this after fixing all log types

        super(SabError, self).__init__(msg)


class SysCommandError(SabError):
    def __init__(self, return_code, cout, cerr, command):
        cout = cout.decode('utf-8')
        cerr = cerr.decode('utf-8')
        self.msg = "System command '%s' returned error code: '%s'\ncout: '%s'\ncerr: '%s'" % (
            command, return_code, cout, cerr)
        self.error_code = ErrorCodes.STUB_ERROR
        self.return_code = return_code
        self.cout = cout
        self.cerr = cerr
        self.interface_err = 'Error in system command (return code is not 0)'
        self.command = command
        super(SabError, self).__init__(self.msg)


class SysCommandTimeout(SabError):
    def __init__(self, command, timeout):
        self.msg = "Command '%s' timed out after %s seconds" % (command, timeout)
        self.error_code = ErrorCodes.STUB_TIMEOUT_ERROR
        self.interface_err = 'SysCommandTimeout'
        self.command = command
        super(SabError, self).__init__(self.msg)


class ValidationError(SabError):
    def __init__(self, target_object, validation_error, error_code):
        self.msg = "Validation error in %s: %s" % (target_object, validation_error)
        self.error_code = error_code
        self.interface_err = "ValidationError"

        super(SabError, self).__init__(self.msg)


class ExitNowAsynCoreLoop(Exception):
    """ Quit an asyncore dispatcher from a handler """
    pass


class SabPoolNotFound(SabError):
    def __init__(self, pool_name=None):
        error = "PoolNotExist"
        interface_err = "problem with updating pool list"
        if pool_name is not None:
            error = "Pool %s not found" % pool_name

        error_code = ErrorCodes.ERROR_SAB_POOL_NOT_FOUND
        super(SabPoolNotFound, self).__init__(error, error_code, interface_err)


class SabAcNotFound(SabError):
    def __init__(self, ac_name=None):
        error = "AcNotExist"
        interface_err = "problem in updating ACC list"
        if ac_name is not None:
            error = "Ac %s not found" % ac_name

        error_code = ErrorCodes.ERROR_SAB_GET_AC_BY_NAME
        super(SabAcNotFound, self).__init__(error, error_code, interface_err)


class SabLunNotFound(SabError):
    def __init__(self, lun_name=None):
        error = "LunNotExist"
        if lun_name is not None:
            error = "Lun %s not found" % lun_name

        error_code = ErrorCodes.ERROR_SAB_LUN_NOT_FOUND
        super(SabLunNotFound, self).__init__(error, error_code, error)


class SabNoRsPool(SabError):
    def __init__(self):
        error = 'Rapidstore pool is not present'
        interface_err = "problem in finding RS Pool"
        error_code = ErrorCodes.SAB_NO_RS_POOL

        super(SabNoRsPool, self).__init__(error, error_code, interface_err)


class ErrorSabGetDiskSlot(SabError):
    def __init__(self, enclosure=None, slot=None):
        error = "DiskNotExist"
        interface_err = "problem with updating disk list"
        if enclosure is not None and slot is not None:
            error = "Disk with enclosure_id:%s and slot_id:%s not found" \
                    % (enclosure, slot)
        error_code = ErrorCodes.ERROR_SAB_GET_DISK_BY_SLOT

        super(ErrorSabGetDiskSlot, self).__init__(error, error_code, interface_err)


class InvalidRaidState(SabError):
    def __init__(self, raid_state):
        error = 'Invalid RAID state: "%s"' % raid_state
        interface_err = "InvalidRaidState"
        error_code = ErrorCodes.INVALID_RAID_STATE

        super(InvalidRaidState, self).__init__(error, error_code, interface_err)


class ErrorHostGetIniName(SabError):
    def __init__(self, name=None):
        error = 'InitiatorNotFound'
        interface_err = 'problem in updating initiator list'
        if name is not None:
            error = 'Initiator %s not found' % name
        error_code = ErrorCodes.ERROR_HOST_GET_INI_BY_NAME

        super(ErrorHostGetIniName, self).__init__(error, error_code, interface_err)


class ErrorRaidDiskNotFound(SabError):
    def __init__(self, enclosure, slot):
        error_code = ErrorCodes.RAID_DISK_NOT_FOUND
        error = "Disk with enclosure and slot %s,%s not found" \
                % (enclosure, slot)
        interface_err = "unknown disk"
        super(ErrorRaidDiskNotFound, self).__init__(error, error_code, interface_err)


class ErrorRaidIdNotFound(SabError):
    def __init__(self):
        error_code = ErrorCodes.ERROR_FIND_RAID_ID
        error = "RAID ID not found."
        interface_err = "unknown RAID"
        super(ErrorRaidIdNotFound, self).__init__(error, error_code, interface_err)


class ErrorRaidFindCacheLunName(SabError):
    def __init__(self, device):
        error = "lun name for cache with path %s not found" \
                % device
        error_code = ErrorCodes.ERROR_RAID_FIND_CACHE_LUN_NAME
        interface_err = "problem with updating cache parameters"
        super(ErrorRaidFindCacheLunName, self).__init__(error, error_code, interface_err)


class ErrorRaidFindCacheLunInstance(SabError):
    def __init__(self, device):
        error = "Cache device with name '%s' not found" \
                % device
        error_code = ErrorCodes.ERROR_RAID_FIND_CACHE_LUN_INSTANCE
        interface_err = "problem with updating cache list"
        super(ErrorRaidFindCacheLunInstance, self).__init__(error, error_code, interface_err)


class RaidNotFoundInPool(SabError):
    def __init__(self, name, raid_id, pool_name):
        error_code = ErrorCodes.RAID_NOT_FOUND_IN_POOL
        error = 'RAID with name and id (%s,%s) not found in pool %s' \
                % (name, raid_id, pool_name)
        interface_err = error
        super(RaidNotFoundInPool, self).__init__(error, error_code, interface_err)


class LunNotFoundInPool(SabError):
    def __init__(self, lun_name, pool_name):
        error_code = ErrorCodes.LUN_NOT_FOUND_IN_POOL
        error = 'LUN %s not found in pool %s' % (lun_name, pool_name)
        interface_err = "problem in updating lun list"
        super(LunNotFoundInPool, self).__init__(error, error_code, interface_err)


class ErrorInvalidDiskInterface(SabError):
    def __init__(self, disk_interface):
        error_code = ErrorCodes.INVALID_DISK_INTERFACE
        error = 'Invalid disk interface: "%s"' % disk_interface
        interface_err = "Invalid disk interface"

        super(ErrorInvalidDiskInterface, self).__init__(error, error_code, interface_err)


class ErrorInvalidDiskConfState(SabError):
    def __init__(self, disk_conf_state):
        error_code = ErrorCodes.INVALID_DISK_CONF_STATE
        error = 'Invalid disk conf state: "%s"' % disk_conf_state
        interface_err = "Invalid disk conf state"
        super(ErrorInvalidDiskConfState, self).__init__(error, error_code, interface_err)


class ErrorInvalidSize(SabError):
    def __init__(self):
        error_code = ErrorCodes.INVALID_SIZE
        error = 'Invalid size'
        interface_err = 'Invalid Size (should end with GB or TB)'
        super(ErrorInvalidSize, self).__init__(error, error_code, interface_err)


class PermissionDenied(SabError):
    def __init__(self):
        error_code = ErrorCodes.ERROR_PERMISSION_DENIED
        error = "PermissionDenied"
        interface_err = "Permission denied"
        super(PermissionDenied, self).__init__(error, error_code, interface_err)


class ErrorNotLogged(SabError):
    def __init__(self):
        error_code = ErrorCodes.ERROR_NOT_LOGGED_IN
        error = "NotLoggedIn"
        interface_err = "User not logged in"
        super(ErrorNotLogged, self).__init__(error, error_code, interface_err)


class ErrorHandlerNotFound(SabError):
    def __init__(self):
        error_code = ErrorCodes.INVALID_URL
        error = "NotFound"
        interface_err = "URL not found"
        super(ErrorHandlerNotFound, self).__init__(error, error_code, interface_err)


class ErrorPerfMonitor(SabError):
    def __init__(self, msg):
        err_code = ErrorCodes.ERROR_PERF_MONITOR
        self.error = msg
        interface_err = 'Error in performance monitoring threads'
        super(ErrorPerfMonitor, self).__init__(msg, err_code, interface_err)


class ErrorLoginHandler(SabError):
    def __init__(self):
        super(ErrorLoginHandler, self).__init__("", -1000)


class ErrorSMTPSetting(SabError):
    def __init__(self, msg, interface_err):
        error_code = ErrorCodes.ERROR_SMTP_SETTING
        interface_err = interface_err
        self.error = msg
        super(ErrorSMTPSetting, self).__init__(self.error, error_code, interface_err)


class SabLunExists(SabError):
    def __init__(self, lun_name):
        error = 'Lun with name %s exists' % lun_name
        interface_err = 'Lun with name %s exists' % lun_name
        error_code = ErrorCodes.SAB_LUN_EXISTS

        super(SabLunExists, self).__init__(error, error_code, interface_err)


class SabPoolExists(SabError):
    def __init__(self, pool_name):
        error = 'Pool with name %s exists' % pool_name
        interface_err = 'Pool with name %s exists' % pool_name
        error_code = ErrorCodes.SAB_POOL_EXISTS

        super(SabPoolExists, self).__init__(error, error_code, interface_err)


class ErrorPMExport(SabError):
    def __init__(self):
        error = 'Can not export pm data'
        interface_err = 'Error in creating performance monitoring excel file'
        error_code = ErrorCodes.ERROR_EXPORT_PM

        super(ErrorPMExport, self).__init__(error, error_code, interface_err)


class ErrorIPConflict(SabError):
    def __init__(self, ip1, network_int):
        error = 'IP(%s) has conflict with IP(%s)' % (str(ip1), str(network_int.get_netmask()))
        interface_err = 'IP(%s) has conflict with IP(%s)' % (str(ip1), str(network_int.get_netmask()))
        error_code = ErrorCodes.ERROR_IP_NETWORK_CONFLICT
        self.conflict_with = network_int.get_name()
        super(ErrorIPConflict, self).__init__(error, error_code, interface_err)


class ErrorLDAPConnection(SabError):
    def __init__(self, msg):
        super(ErrorLDAPConnection, self).__init__(msg, ErrorCodes.ERROR_LDAP_CONNECTION, "Error in LDAP connection")


class ErrorLDAPLogin(SabError):
    def __init__(self):
        msg = "Illegal user or pass"
        super(ErrorLDAPLogin, self).__init__(msg, ErrorCodes.ERROR_LDAP_LOGIN, "Error in login to LDAP")


class ErrorTestLDAPConfig(SabError):
    def __init__(self, msg, interface_err):
        error_code = ErrorCodes.ERROR_SMTP_SETTING
        interface_err = interface_err
        self.error = msg
        super(ErrorTestLDAPConfig, self).__init__(self.error, error_code, interface_err)


class ErrorLDAPConfig(SabError):
    def __init__(self):
        msg = "LDAP Configuration not found in Database"
        super(ErrorLDAPConfig, self).__init__(msg, ErrorCodes.ERROR_LDAP_CONFIG_TABLE, "unknown LDAP configuration")


class ErrorLDAPUserNotFound(SabError):
    def __init__(self, user):
        msg = "Username '%s' not found in the LDAP server" % user
        super(ErrorLDAPUserNotFound, self).__init__(msg, ErrorCodes.ERROR_LDAP_INVALID_USER, msg)


class ErrorLDAPDefRole(SabError):
    def __init__(self):
        msg = "Default role name not exists for LDAP"
        super(ErrorLDAPDefRole, self).__init__(msg, ErrorCodes.ERROR_LDAP_DEF_ROLE_NOT_FOUND, msg)


class ErrorInvalidName(SabError):
    def __init__(self, name):
        msg = "Name '%s' is not valid" % name
        super(ErrorInvalidName, self).__init__(msg, ErrorCodes.ERROR_INVALID_NAME, "General error for invalid name")


class ErrorESXServer(SabError):
    def __init__(self, server_address, server_port):
        msg = "%s:%s is not an ESX/vCenter server" % (str(server_address), str(server_port))
        super(ErrorESXServer, self).__init__(msg, ErrorCodes.ERROR_ESX_ADDRESS, "ErrEsxAddress")


class ErrorESXAuthentication(SabError):
    def __init__(self):
        msg = "Could not connect to the specified host using specified username and password"
        super(ErrorESXAuthentication, self).__init__(msg, ErrorCodes.ERROR_ESX_AUTH, "ErrEsxUserPass")


class ErrorFileSystem(SabError):
    def __init__(self, msg, err_code):
        super(ErrorFileSystem, self).__init__(msg, err_code)


class SabFSExists(SabError):
    def __init__(self, name):
        msg = "Filesystem '%s' already exists" % name
        interface_err = 'Filesystem with name %s exists' % name
        super(SabFSExists, self).__init__(msg, ErrorCodes.ERROR_DUPLICATED_FILE_SYSTEM, interface_err)


class ErrorShare(SabError):
    def __init__(self, msg, err):
        super(ErrorShare, self).__init__(msg, err, msg)


class ErrorWinShare(ErrorShare):
    def __init__(self, msg, err):
        super(ErrorWinShare, self).__init__(msg, err)


class ErrorNFSShare(ErrorShare):
    def __init__(self, msg, err):
        super(ErrorNFSShare, self).__init__(msg, err)


class ErrorSnapshot(SabError):
    def __init__(self, msg, err):
        super(ErrorSnapshot, self).__init__(msg, err)


class SabSnapshotNotFound(SabError):
    def __init__(self, lun_name=None):
        error = "SnapshotNotExist"
        if lun_name is not None:
            error = "Snapshot %s not found" % lun_name

        error_code = ErrorCodes.ERROR_SAB_SNAPSHOT_NOT_FOUND
        super(SabSnapshotNotFound, self).__init__(error, error_code, error)


class SabRestrictionAccessDenied(Exception):
    pass
