# -*- coding: utf-8 -*-
"""Schemas module

This module defines data schemas for validating properties coming through
the trackers.
"""
CLIENT_TYPES = ('mobile', 'web')
AUTH_TYPES = ('basic', 'saml')
ACTION_TYPES = ('view', 'create', 'edit', 'delete', 'restore')
WF_ACTION_TYPES = ('any', 'create', 'edit', 'delete', 'scheduled',
                   'parent_associated', 'parent_dissociated',
                   'child_associated', 'child_dissociated')
WF_STATUS = ('start', 'done')
AGENT_TYPES = ('api', 'connector', 'import', 'ticket_plugin', 'webui', 'wf',
               'jit', 'saas')
OBJECT_TYPES = ('accessories', 'assets', 'audits', 'contracts', 'locations',
                'users', 'saas', 'software', 'stockrooms')
SYSTEM_TYPES = ('demo', 'dev', 'poc', 'prod', 'sandbox')


USER_SCHEMA = {
    'full_name': {
        'type': 'string',
        'required': True,
        'nullable': True  # 'empty' default is True
    },
    'role': {
        'type': 'string',
        'required': True,
        'nullable': True
    },
    'server': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    }
}


UPLOAD_SCHEMA = {
    'server': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    }
}


USER_UPLOAD_SCHEMA = {
    'user_id': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'full_name': {
        'type': 'string',
        'required': True,
        'nullable': True
    },
    'role': {
        'type': 'string',
        'required': True,
        'nullable': True
    }
}


LOGIN_SCHEMA = {
    'client_type': {
        'type': 'string',
        'allowed': CLIENT_TYPES,
        'required': True
    },
    'auth_type': {
        'type': 'string',
        'allowed': AUTH_TYPES,
        'required': True
    },
    'identity_provider': {
        'type': 'string',
        'required': True,
        'nullable': True  # 'empty' default is True
    },
    'server': {
        'type': 'string',
        'required': True,
        'empty': False  # 'nullable' default is False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    }
}

WORKFLOW_RUN_SCHEMA = {
    'run_id': {
        'type': 'integer',
        'required': True
    },
    'wf_id': {
        'type': 'integer',
        'required': True
    },
    'wf_name': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'action_type': {
        'type': 'string',
        'required': True,
        'allowed': WF_ACTION_TYPES
    },
    'object_type': {
        'type': 'string',
        'required': True,
        'allowed': OBJECT_TYPES
    },
    'status': {
        'type': 'string',
        'required': True,
        'allowed': WF_STATUS
    },
    'server': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    }
}

OBJECT_ACTION_SCHEMA = {
    'action_type': {
        'type': 'string',
        'required': True,
        'allowed': ACTION_TYPES
    },
    'agent_type': {
        'type': 'string',
        'required': True,
        'allowed': AGENT_TYPES
    },
    'agent_name': {
        'type': 'string',
        'required': True,
        'nullable': True  # 'empty' default is True
    },
    'object_type': {
        'type': 'string',
        'required': True,
        'allowed': OBJECT_TYPES
    },
    'server': {
        'type': 'string',
        'required': True,
        'empty': False
    },
    'system_type': {
        'type': 'string',
        'allowed': SYSTEM_TYPES,
        'required': True
    }
}