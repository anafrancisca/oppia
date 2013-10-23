// Copyright 2012 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS-IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/**
 * @fileoverview Service for sending messages to a parent iframe. All outbound
 * communication with a parent iframe should pass through here. (This
 * communication should be outbound only; reverse communication should NOT
 * be attempted due to cross-domain security issues.)
 *
 * @author sll@google.com (Sean Lip)
 */

oppia.factory('messengerService', function() {
  var isPositiveInteger = function(n) {
    return (typeof n === 'number' && n % 1 === 0 && n > 0);
  };

  MESSAGE_VALIDATORS = {
    'heightChange': function(payload) {
      return isPositiveInteger(payload.height);
    },
    'explorationCompleted': function(payload) {
      return true;
    }
  };

  var getPayload = {
    'heightChange': function(data) {
      return {height: data};
    },
    'explorationCompleted': function(data) {
      return {};
    }
  };

  var messenger = {
    HEIGHT_CHANGE: 'heightChange',
    EXPLORATION_COMPLETED: 'explorationCompleted',
    sendMessage: function(messageTitle, messageData) {
      // Only send a message if the oppia window is iframed.
      if (window.parent != window &&
          MESSAGE_VALIDATORS.hasOwnProperty(messageTitle)) {
        var idAndVersionHash = window.location.hash.substring(1);
        if (idAndVersionHash.indexOf('&') === -1) {
          console.log(
              'Embedding error: Invalid id/version hash: ' + idAndVersionHash);
        }

        var separatorLocation = idAndVersionHash.indexOf('&');

        var sourceTagId = idAndVersionHash.substring(0, separatorLocation);
        var version = idAndVersionHash.substring(separatorLocation + 1);

        if (version == '0.0.0') {
          console.log('Posting message to parent: ' + messageTitle);

          var payload = getPayload[messageTitle](messageData);
          if (!MESSAGE_VALIDATORS[messageTitle](payload)) {
            console.log('Error validating payload: ' + payload);
          }

          window.parent.postMessage(
            {title: messageTitle, payload: payload, sourceTagId: sourceTagId},
            '*');
        }
      }
    }
  };

  return messenger;
});