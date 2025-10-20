/*!
#########################################################
# ORA_MYSQL.JS
# Version: 1.00
# BUILD DATE: Thursay 5-Jan-2023 (Pacific Daylight Time)
# COPYRIGHT ORACLE CORP 20223 [UNLESS STATED OTHERWISE]
#########################################################
*/

/*! Checking to see if the user has set the cookie consent, using TrustArch */
/* Include the oracle.truste.api code - This comes from PDIT, richa.kamal@oracle.com and can be found at
URL: http://www.oracle.com/us/assets/truste-oraclelib.js 

Look to see if oracle.truste.api.getConsentCode() fucntion exist and if not load it...
*/
try {
    oracle.truste.api.getConsentDecision().consentDecision;
    oracle.truste.api.getConsentDecision().source;
    } catch(err) {
var oracle=oracle||{};oracle.truste={};oracle.truste.api={};(function(){var trusteCookieName="notice_preferences";var trusteStorageItemName="truste.eu.cookie.notice_preferences";this.getCookieName=function(){return trusteCookieName;};this.getStorageItemName=function(){return trusteStorageItemName;};}).apply(oracle.truste);(function(){var trusteCommon=oracle.truste;function getCookie(cookieKey){var name=cookieKey+"=";var cookieArray=document.cookie.split(";");for(var i=0;i<cookieArray.length;i++){var c=cookieArray[i];while(c.charAt(0)==" "){c=c.substring(1);}if(c.indexOf(name)==0){return c.substring(name.length,c.length);}}return null;}function getLocalStorageItem(storageKey){if(typeof(Storage)!=="undefined"){return localStorage.getItem(storageKey);}return null;}function getTRUSTeLocalStorageValue(storageKey){var value=getLocalStorageItem(storageKey);if(value!=null){var obj=JSON.parse(value);return obj.value;}return null;}this.getConsentCode=function(){var value=getTRUSTeLocalStorageValue(trusteCommon.getStorageItemName())||getCookie(trusteCommon.getCookieName());if(value==null){return -1;}else{return parseInt(value)+1;}};this.getConsentDecision=function(){var value=this.getConsentCode();if(value==-1){var text='{"consentDecision": 0, "source": "implied"}';return JSON.parse(text);}else{var text='{"consentDecision": '+parseInt(value)+', "source": "asserted"}';return JSON.parse(text);}};}).apply(oracle.truste.api);
}

var TRUSTeLevel = s_setConsentLevel(0);

/* TRUSTe and cookie functions...

CONSENT LEVEL -  0 = Not yet chosen to manage the consent level
			  -  1 = required ONLY, don't send any PING's.
			  -  2 = required + functional, can sent PING for Eloqua and Site Catalyst
			  -  3 = required + functional + advertising, can send PING Eloqua and Site Catalyst and any advertising tags
*/             
function s_setConsentLevel(cLevel) {
/* The function tries to look up the truste.cma.callApi. If that fails then look at the Oracle 1st party cookie that get gets set by the TRUSTe manage [notice_preferences]. This cookie's first value represents the preference set [in "1:cb8350a2759273dccf1e483791e6f8fd" the "1" is the same as the CONSENT LEVEL "2" (i.e. cookie + 1 = CONSENT LEVEL].

If none of these methods return a value it is assumed that the users has NOT managed their preferences, and so the default value of CONSENT LEVEL = 0 is set...

*/
    try {
        cLevel = truste.cma.callApi("getConsentDecision","oracle.com").consentDecision;
    }catch(err){
        cLevel = s_getCookieData("notice_preferences").split(":")[0]
        if (cLevel == "") {
            cLevel = 0;
        }else{
            cLevel = ++cLevel;
        }    
    }
    return cLevel;
}
    
function s_getCookieData(label){
	var labelLen = label.length;
	var cLen = document.cookie.length;
	var i = 0;
	var cEnd;
	while(i < cLen){
		var j=i+labelLen;
		if (document.cookie.substring(i,j) == label){
			cEnd=document.cookie.indexOf(";",j);
			if (cEnd==-1){
				cEnd=document.cookie.length;
			}
			j++;
			return decodeURIComponent(document.cookie.substring(j,cEnd).replace("+","%20"));
		}
		i++;
	}
	return "";
}

/*! Script to check Do Not Track settings in the browser */
// Variable to store browser tracking settings.
var enable_tracking = true;
if(TRUSTeLevel == -1 || TRUSTeLevel == 0) { // If Truste consent is implied, check DNT settings.
	// Check if Do Not Track settings is enabled in the browser.
	if(navigator.doNotTrack == 1 || window.doNotTrack == 1 || navigator.msDoNotTrack == 1) {
		enable_tracking = false;
	}
} else if(TRUSTeLevel == 1) {
	enable_tracking = false;
}

// Setting up the report suite and site ID, this function is used in ora_code.js
function s_setAccount(){
/* Set the default values in the array 'sa' 														*/
var sa=["sunmysqldev","mysql","en-us"];

/* Check to see if the site is STAGE or DEV or LOCAL or from webstandards-us.oracle.com 			*/
/* then set the Site Catalyst report suite to either DEV or PROD									*/

	if (location.host.indexOf("stage") != -1 || 
	    location.host.indexOf("-dev") != -1 || 
		location.host.indexOf("mysqldev") != -1 || 
		location.host.indexOf("localhost") != -1)
	 { sa[0] = "sunmysqldev"; } 
	else 
	 { sa[0] = "sunmysql"; }
	 
/* Return the array 'sa' with [RSID, siteID, language-country]										*/
return sa;
}

// If OK to send the ping, then injected the tracking scripts into the page //
if (enable_tracking){

// Old version of the set-up scripts - commented out...
	/* Specify the Report Suite(s) */
	//    var s_account="sunmysqldev";
	//    var sun_dynamicAccountSelection=true;
	//    var sun_dynamicAccountList="sunmysql=mysql.com;sunmysql=mysql.de;sunmysql=mysql.fr;sunmysql=mysql.it;sunmysqldev=.";
    /* Specify the Site ID */
	//    var s_siteid="mysql:";
	
/* Check to see if the URL is http OR https */
	var host_type = (window.location.protocol.toLowerCase().indexOf("https")!=-1) ? 'https' : 'http';
	var ora_global = "://www.oracle.com/us/assets/metrics/ora_code.js"
 /* Run the local and global ora_code.js file */
    var scFiles = [host_type + ora_global]
    scFiles.forEach(function(src) {
      var scScript = document.createElement('script');
      scScript.src = src;
      scScript.async = false;
      document.body.appendChild(scScript);
    });
}

// Old version of the set-up scripts - commented out...
	/* Omniture JS call  */
	//    var sun_ssl=(window.location.protocol.toLowerCase().indexOf("https")!=-1);
	//        if(sun_ssl == true) { var fullURL = "https://www.oracle.com/us/assets/metrics/ora_code.js"; }
	//            else { var fullURL= "https://www.oracle.com/us/assets/metrics/ora_code.js"; }
	//    document.write("<sc" + "ript type=\"text/javascript\" src=\""+fullURL+"\"></sc" + "ript>");

// prePlugin function to set the s_pageName, which overrides the ora_code.js page naming.
function s_prePlugins(s) {
	
	// Set the javascript code version, was s.prop33 now s.prop55 (set inora_code.js)
    s_oraVer(":mysql", ":1.00");

    /* PageName Settings */
	var mysql_host=location.hostname;
    if (mysql_host=='dev.mysql.com') {
        var mysql_url=window.location.pathname.toLowerCase();
        var mysql_split=mysql_url.split("/");
    }
	
    if (typeof s_pageType=='undefined') {
        var s_pageName=window.location.host+window.location.pathname;
        s_pageName=s_pageName.replace(/www.mysql.com/,"");
        s_pageName=s_pageName.replace(/www.mysql./,"");
        s_pageName=s_pageName.replace(/.mysql.com/,":");
        s_pageName=s_pageName.replace(/mysql.com/,"");
    }
	
	s_account[1] = (location.hostname=='dev.mysql.com') ? "mysql:dev" : s_account[1]
	s_account[1] = (location.hostname=='list.mysql.com') ? "mysql:list" : s_account[1]
	
	s_pageName = s_account[1] + ":" + s_pageName
	
}

/* Clean up pageName and set legacy props31, eVar35 */ 
function s_postPlugins(s) {
	
	s.pageName = s.pageName.replace("en-us:","");
	s.channel = s.pageName
	
	var mysql_host=location.hostname;
	var mysql_url=window.location.pathname.toLowerCase();
    var mysql_split=mysql_url.split("/");
	
    /* dev.mysql.com/doc ---> prop31  */
    if (mysql_host=='dev.mysql.com') {
        if (mysql_split[1]=="doc") {
            s.prop31=s.pageName;
            s.channel=s.channel+" (site section)";
            }
        }
    /* lists.mysql.com ---> prop31  */
        if (mysql_host=='lists.mysql.com') {
            s.prop31=s.pageName;
            s.channel=s.channel+" (site section)";
		}

	// Set prop31 to the pageName for backward compatability
	s.prop31=s.pageName;
	// Set eVar35 to be the URL
	s.eVar35=location.href;
	s.eVar35=s.eVar35.replace(/;jsessionid.*$/,'');
	s.eVar35=s.eVar35.replace(/jsessionid.*$/,'');
	
	/* Set Date Stamp - based on UTC*/
	var s_date=new Date();
	var s_hour=s_date.getUTCHours();
	var s_minute=s_date.getUTCMinutes();
	var s_seconds=s_date.getUTCSeconds();
	if (s_hour < 10) { s_hour="0"+s_hour }
	if (s_minute < 10) { s_minute="0"+s_minute }
	if (s_seconds < 10) { s_seconds="0"+s_seconds }
	var s_time=s_hour+":"+s_minute+":"+s_seconds;
	s.prop44=s_time;
}

// Function to set the JavaScript code version
function s_oraVer(_s, _v) {
    _v = _s + _v;
    oraVersion = (oraVersion.indexOf(_s) == -1) ? oraVersion + _v : oraVersion.substr(0, oraVersion.indexOf(_s)) + _v;
}	
