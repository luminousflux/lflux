/**
 * Initializing the namespace MessageBoxes that includes the modal window functions
 */
var MessageBoxes = 
{
		/**
   		 * ID of the Container that is used for the message boxes
		 */
		ALERT_CONFIRM_CONTAINER : 'divAlertConfirmContainer',

		/**
		 * Opens an Alert
		 * 
		 * @param msg string 	message to show
		 * @param ttl string 	title of the alert window (default: "Message")
		 * @param modal bool	defines whether the alert should be shown as a modal window
		 */
		Alert : function(msg, ttl, modal)
		{
			if(!ttl)
			{
				var ttl = "Message";
			}
			
			if(typeof(modal) != 'boolean')
			{
				modal = true;
			}
			
			var options = { 'modal' : modal };
			
			MessageBoxes._showModal(msg, ttl, 
					{
						Ok : function()
						{
							$(this).dialog('close');
						}
					}, options);
			// Initialize Enter and Esacpe keypress events
			MessageBoxes._initKeyDownEvents();
		},
		
		/**
		 * Opens a Confirm
		 * 
		 * @param msg string 		message to show
		 * @param ttl string 		title of the confirm window (Default: "Question")
		 * @param callback function 	callback Funktion that is executed after user interaction and called with a boolean parameter (true = OK-Button, false = Cancel-Button)
		 * @param modal bool		defines whether the alert should be shown as a modal window
		 */
		Confirm : function(msg,ttl,callback,modal)
		{
			if(!ttl)
			{
				var ttl = "Question";
			}
			
			if(typeof(modal) != 'boolean')
			{
				modal = true;
			}
			
			var options = { 'modal' : modal };
			
			var doCallback = (callback && typeof(callback) == 'function');
			
			MessageBoxes._showModal(msg, ttl, 
					{
						Yes : function()
						{
							$(this).dialog('close');
							if(doCallback)
							{
								callback(true);
							}
						},
						No : function()
						{
							$(this).dialog('close');
							if(doCallback)
							{
								callback(false);
							}
						}
					},options);
			
			MessageBoxes._initKeyDownEvents(callback);
		},
		
		/**
		 * Shows an extended prompt dialog by providing the possibility for
		 * several form inputs (textarea, select, input)
		 *
		 * @param msg string		message to show
		 * @param ttl string		title of the modal window
		 * @param fields Array		an array that defines the form inputs ({ label : string, type : string, name : string, items : Array {value : string, text : string})
		 * @param callback function	callback function that is executed after user interaction, by clicking OK the function is called with an object of field-value pairs (e.g. { name : 'thomas', address : 'at home' })
		 */
		Prompt : function(msg, ttl, fields, callback)
		{
			var html = '<div>' + msg + '</div>';
			
			var i;
            // iritate over defined fields
			for(i = 0; i < fields.length; i++)
			{
				html += '<div>';
                // Check for a label/caption
				if(fields[i].label != '')
				{
					html += '<label for="prompt_'+fields[i].name+'">'+fields[i].label+'</label>';
				}
                // Check the type of the form input
				if(fields[i].type == 'textarea') //Multinline textbox
				{
					html += '<textarea id="prompt_'+fields[i].name+'" cols="35" rows="5" style="width:97%;"></textarea>';
				}
				else if(fields[i].type == 'select') //Dropdown box
				{
					html += '<select id="prompt_'+fields[i].name+'">';
					var j = 0;
					var items = fields[i].items;
					for(j = 0; j < items.length; j++)
					{
						html += '<option value="'+items[j].value+'">' + items[j].text + '</option>'; 
					}
					html += '</select>';
				}
				else //Other inputs (checkbox, text)
				{
					html += '<input id="prompt_'+fields[i].name+'" type="'+fields[i].type+'" />';
				}
				html += '</div>';
			}
			
            //Check whether to execute the callback function
			var doCallback = (callback && typeof(callback) == 'function');
			
			MessageBoxes._showModal(html, ttl, 
						{
							Ok : function()
							{
								$(this).dialog('close');
								if(doCallback)
								{
                                    // Write the values of the prompt into an object
									var result = new Object();
									for(i = 0; i < fields.length; i++)
									{
										result[fields[i].name] = $('#prompt_' + fields[i].name).val();
									}
                                    // Call callback function with user input
									callback(result);
								}
							},
							Cancel : function()
							{
								$(this).dialog('close');
								if(doCallback)
								{
                                    // Escape / Cancel
									callback(false);
								}
							}
						});
			
            // Set the focus to the first input form element
			$('#'+ MessageBoxes.ALERT_CONFIRM_CONTAINER + ' input:first').focus();
			
            // Bind the keydown events for enter and escape press
			$(window).bind('keydown.alert',function(e)
			{
				if(e.keyCode == 13)
				{
					MessageBoxes.CloseAlert();
					var result = new Object();
					for(i = 0; i < fields.length; i++)
					{
						result[fields[i].name] = $('#prompt_' + fields[i].name).val();
					}
					callback(result);
				}
				else if(e.keyCode == 27)
				{
					MessageBoxes.CloseAlert();
					$(window).unbind('keydown.alert');
					if(doCallback) callback(false);
				}
			});
		},
		
		/**
		 * Closes the modal windows
		 */
		CloseAlert : function()
		{
			$('#'+MessageBoxes.ALERT_CONFIRM_CONTAINER).dialog('close');
		},
		
		/**
   		 * Shows a modal window by using jQuery UI dialog
		 *
		 * @param msg string		message to show
		 * @param ttl string		title of the window
		 * @param btns Array		array with buttons
		 * @param options object	additional options (see: http://docs.jquery.com/UI/Dialog#options)
		 */
		_showModal : function(msg,ttl,btns,options)
		{
            // The default options
			var defaultOptions = {
				title : ttl,
				buttons : btns,
				modal : true,
				resizable : false,
				draggable : false,
				close : function()
				{
					$(this).dialog('destroy');
				}
			};
            // Container with the modal window
			var div = $('#'+MessageBoxes.ALERT_CONFIRM_CONTAINER);
			if(div.length <= 0)
			{
				div = $('<div id="'+MessageBoxes.ALERT_CONFIRM_CONTAINER+'" />').appendTo('body');
			}
			
            // Extended options
			if(options)
			{
				options = $.extend(options, defaultOptions);
			}
			else
			{
				var options = defaultOptions;
			}
			
			div.html(msg);

            $(div).find('textarea').bind('keydown.alert', function(e) {
                    e.stopPropagation();
                    return true;
                    });
			
            // Initialize jQuery dialog
			div.dialog(
				options
			);
		},
		
		/**
  		 * Initializes an event to be triggered when Enter or Escape is pressed
         *
		 * @param callback function	triggered function
		 */
		_initKeyDownEvents : function(callback)
		{
			var doCallback = (callback && typeof(callback) == 'function');
            // Bind namespaced event (see: http://docs.jquery.com/Namespaced_Events )
			$(window).bind('keydown.alert',function(e)
			{
				if(e.keyCode == 13) // Enter
				{
					MessageBoxes.CloseAlert();
					$(window).unbind('keydown.alert');
					if(doCallback) callback(true);
				}
				else if(e.keyCode == 27) // Escape
				{
					MessageBoxes.CloseAlert();
					$(window).unbind('keydown.alert');
					if(doCallback) callback(false);
				}
			});
		}
};
