Name:       ibus-typing-booster
Version:    1.5.14
Release:    1%{?dist}
Summary:    A completion input method
License:    GPLv3+
Group:      System Environment/Libraries
URL:        https://mike-fabian.github.io/ibus-typing-booster/
Source0:    https://fedorahosted.org/releases/i/b/ibus-typing-booster/%{name}-%{version}.tar.gz
Requires:   ibus >= 1.5.3
Requires:   m17n-lib
Requires:   python3 >= 3.3
Requires:   python3-dbus
Requires:   python3-enchant
# Recommend a reasonably good font which has most of the emoji:
Recommends: gdouros-symbola-fonts
BuildRequires:  ibus-devel
BuildRequires:  python3-devel
# for the unit tests
BuildRequires:  m17n-lib
BuildRequires:  m17n-db-extras
BuildRequires:  python3-enchant
BuildRequires:  hunspell-cs
BuildRequires:  hunspell-de
BuildRequires:  hunspell-en
BuildRequires:  hunspell-es
BuildRequires:  hunspell-it
BuildRequires:  hunspell-ko
BuildArch:  noarch

%description
Ibus-typing-booster is a context sensitive completion
input method to speedup typing.

%prep
%setup -q


%build
export PYTHON=%{__python3}
%configure --disable-static --disable-additional
make %{?_smp_mflags}

%install 
export PYTHON=%{__python3}
make install DESTDIR=${RPM_BUILD_ROOT} NO_INDEX=true  INSTALL="install -p"   pkgconfigdir=%{_datadir}/pkgconfig
gzip --force --best $RPM_BUILD_ROOT/%{_datadir}/%{name}/data/*.{xml,txt,json}

%find_lang %{name}

%check
export LC_ALL=en_US.UTF-8
desktop-file-validate \
    $RPM_BUILD_ROOT%{_datadir}/applications/ibus-setup-typing-booster.desktop
pushd engine
    # run doctests
    python3 hunspell_suggest.py
    python3 m17n_translit.py
    python3 itb_emoji.py
    python3 itb_util.py
popd
eval $(dbus-launch --sh-syntax)
dconf dump /
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/offtherecord false
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/usedigitsasselectkeys true
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/tabenable false
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/inputmethod "'NoIme'"
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/adddirectinput false
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/rememberlastusedpreeditime true
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/mincharcomplete 1
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/dictionary "'en_US'"
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/emojipredictions true
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/autocommitcharacters "''"
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/pagesize 6
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/shownumberofcandidates true
dconf write /desktop/ibus/engine/typing-booster/typing-booster-de-de/showstatusinfoinaux true
dconf dump /
ibus-daemon -drx
make check || cat ./tests/test-suite.log

%post
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%postun
[ -x %{_bindir}/ibus ] && \
  %{_bindir}/ibus write-cache --system &>/dev/null || :

%files -f %{name}.lang
%doc AUTHORS COPYING README 
%{_datadir}/%{name}
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/ibus/component/typing-booster.xml
%{_libexecdir}/ibus-engine-typing-booster
%{_libexecdir}/ibus-setup-typing-booster
%{_datadir}/pkgconfig/%{name}.pc
%{_datadir}/applications/ibus-setup-typing-booster.desktop

%changelog
* Fri Nov 25 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.14-1
- update to 1.5.14
- Reopen preëdit not only on Backspace but also on Delete and arrow keys
- Fix "delete whitespace when committing punctuation" problem in firefox
  Resolves rhbz#1399192
- Add pt_BR translations from zanata. Update uk, pl, and de translations from zanata.
- Add an option to show/hide the status information in the auxiliary text
- Use ballot box characters in front of the mode indicators in the auxiliary text

* Mon Nov 21 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.13-1
- update to 1.5.13
- Update French translations from zanata

* Sun Nov 20 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.12-1
- update to 1.5.12
- Display existing shortcuts and make it possible to delete them
- Update translations from zanata (de, pl, uk)

* Thu Nov 17 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.11-1
- update to 1.5.11
- Add feature to define custom shortcuts
- Merge editor and tabengine classes

* Wed Nov 09 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.10-1
- update to 1.5.10
- Make accent insensitive matching also work in the user database
- Add test cases for accent insensitive matching
- Add 'No' (Number, Other) to VALID_CATEGORIES to be able to
  match ¹ U+00B9 SUPERSCRIPT ONE

* Mon Oct 24 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.9-1
- update to 1.5.9
- Make it possible to use a database in different locations than the default
- Clear candidate list as well when clearing the lookup table
- Add missing CLDR xml files to tar ball
- Add unit tests

* Mon Oct 10 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.8-1
- update to 1.5.8
- Pull translations from Zanata (uk and fr updated)
- Match many more Unicode characters in the emoji matcher
- Make it possible to match Unicode characters by typing the hexadecimal code point
- If one tries to set a non-existing input method, don’t crash,
  only print an error in the debug log
- Add key and mouse bindings for “Off the record” mode to README

* Mon Sep 19 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.7-1
- update to 1.5.7
- Pull translations from Zanata (de, pl, uk updated)
- Make the list of characters to auto commit configurable
  (Empty list by default)
- Fix duplicates in the candidate list caused by overwriting
  input_phrase with the NFC version
- Don’t show the special candidates for missing dictionaries for
  Japanese and Chinese
- Implement do_cursor_up() and do_cursor_down() to make scrolling
  the lookup table with the mouse wheel work (Needs also a patch in ibus)
- Add an “Off the record mode” (also gets a property menu)
- Tooltips don’t seem to work on sub-properties, remove the tooltips there
- Add a property menu for the emoji prediction mode
- Make triggering a commit with “Left” or “Control+Left” work
  correctly in “Tab enable mode ” again
- Down, Up, Page_Down, and Page_Up should trigger a commit and
  be passed to the application if possible
- If “☑ Enable suggestions by Tab key” is on make it possible
  to close the lookup table with Escape but keep the preëdit
- If “☑ Enable suggestions by Tab key” is on, don’t autocommit digits
- Make autocommitting much more rare (for characters which are not
  the first typed character)
- Don’t autocommit the first typed character unless absolutely necessary
- Even when “☑ Enable suggestions by Tab key” is used,
  don’t complete empty strings

* Mon Sep 12 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.6-1
- update to 1.5.6
- Reduce the number of characters which cause immediate commits a lot
- Load CLDR data for *all* languages in the _expand_languages() list
- Currency symbols should neither be stripped from tokens nor
  trigger an immediate commit
- Fix bidi reordering problem in the candidate list for
  right-to-left candidates followed by comments
- Update emoji annotations from CLDR (de_CH and sr_Latn new,
  the others updated)
- Remove category 'Pc' from categories to commit immediately
  (allow _ to be typed into the preëdit always)
- Remove button to install pyhunspell from the setup tool
  (python3-enchant is preferred and even required by the Fedora rpm)
- Include more currency symbols and fullwidth symbols
- Add category from UnicodeData.txt to emoji dictionary
  (For better results when looking up related characters)
- Add 'Sc', # Symbol, Currency to VALID_CATEGORIES
  (to make the currency symbols work)
- Add list of valid characters (to include special characters
  manually)
- Add mouse binding Alt+Mouse3 anywhere in the candidate list
  to start the setup tool

* Sat Sep 10 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.5-1
- update to 1.5.5
- Pull translations form Zanata (de, pl, and uk updated because of
  the new “About” tab)
- If “☑ Enable suggestions by Tab key” option is on, any preëdit
  change should hide the lookup table
- Make showing of similar emoji work even if emoji preditions are off
- Display whether emoji predictions are turned on in the auxiliary string
- Add key and mouse bindings to toggle the emoji predictions
  (AltGr+F6 and Control+Mouse3 anywhere in the candidate list)
- Add AltGr+F10 key binding to open the setup tool
- Allow any amount of white space and '_' characters to seperate words
  in an emoji query string
- Add an “About” tab to the setup tool and put links to home page and
  online documentation there.
- Update README with latest key binding and mouse binding documentation

* Thu Sep 08 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.4-1
- update to 1.5.4
- Accent insensitive matching
- Update pl.po from zanata
- Add cache for the suggestions from the hunspell dictionaries
- Make Control+MouseButton1 remove the clicked candidate from
  the user database (was MouseButton2)
- Change key binding for looking up related candidates
  from Alt+F12 to AltGr+F12
- Change label of the emoji option to
  “☑ Unicode symbols and emoji predictions”

* Sat Sep 03 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.3-1
- update to 1.5.3
- Pull translations from Zanata: updates for pl and uk.
- Fix behaviour of the option “Minimum number of chars for completion”

* Fri Sep 02 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.2-1
- update to 1.5.2
- get_supported_imes(self) and def get_current_imes(self) should
  return copies not the lists directly
- Resolves: rhbz#1372660
- Update emojione.json, version from 2016-07-16
- Pull translations from Zanata: Fixes for fr and pl. New: uk
- Changes in itb_emoji.py necessary because of the update of
  the CLDR emoji annotations.
- Update emoji annotations from CLDR (be, bs, cy, eu, gl, zu
  are new, the others updated).
- Shortcut keys which look up related candidates should enable
  the candidate list
- Show ⏳ HOURGLASS WITH FLOWING SAND in the auxiliary text when
  the lookup table is being updated
- Fix bug when committing the preëdit with Space when no
  candidates are available
- Improve the behaviour of the “Tab” key
- Improve the behaviour of the “Escape” key.
- Make mouse clicks in the candidate list behave differently
  depending on the mouse button
- Add hu-rovas-post.mim to hu_HU.conf

* Fri Aug 12 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.1-1
- update to 1.5.1
- If the query string in EmojiMatcher.candidates() is an emoji
  itself, match similar ones (useful when backspacing to an emoji
  to correct it)                          
- Data files should not be stored gzipped in the repository
- Change displayed input method name from “Hunspell” to “Typing Booster”
- Use Zanata to get more translations
- French translations added (100% translated)
- Polish translations added (100% translated)
- Add Recommends: gdouros-symbola-fonts

* Thu Aug 11 2016 Mike FABIAN <mfabian@redhat.com> - 1.5.0-1
- update to 1.5.0
- If the lookup table shows related words, “Escape” shows the
  original lookup table
- Use itb_nltk.py to find related words (synonyms, hypernyms, and hyponyms)
- Add a module to find related words using NLTK
- Add a feature to find similar emoji
- Add predictions for emoji (optional, on by default)
- Add a module to match emoji using Unicode, CLDR, and emojione data
- Make typing-booster.appdata.xml translatable
- When ignoring key release events, “False” should be returned, not “True”
- Resolves: rhbz#1365497
- Make typing smoother by updating the candidates using GLib.idle_add()
- Make it possible to enter a space into the preëdit by
  typing “G- ” (AltGr+Space)

* Sun Jul 17 2016 Mike FABIAN <mfabian@redhat.com> - 1.4.8-1
- update to 1.4.8
- Commit preëdit if modifier keys without transliteration are
  typed and pass the key through
- Resolves: rhbz#1351748 in a better way

* Mon Jul 11 2016 Mike FABIAN <mfabian@redhat.com> - 1.4.7-1
- update to 1.4.7
- Check if the commit key would change the transliteration if
  used as regular input
- Resolves: rhbz#1353672 

* Fri Jul 01 2016 Mike FABIAN <mfabian@redhat.com> - 1.4.6-1
- update to 1.4.6
- Pass modifier key combinations through if there is no possible
  transliteration for that key combination
- Resolves: rhbz#1351748

* Wed May 11 2016 Mike FABIAN <mfabian@redhat.com> - 1.4.5-1
- update to 1.4.5
- Do not colourize the preëdit dark blue, that is unreadable on
  dark backgrounds
- Resolves: rhbz#1335201
- Set the size of the libm17n mconv conversion buffer correctly
- Resolves: rhbz#1335021

* Tue May 10 2016 Mike FABIAN <mfabian@redhat.com> - 1.4.4-1
- update to 1.4.4
- self._current_imes needs to be updated before self.init_transliterators()
- Resolves: rhbz#1334579

* Thu Apr 28 2016 Mike FABIAN <mfabian@redhat.com> - 1.4.3-1
- update to 1.4.3
- Fix AttributeError: 'editor' object has no attribute 'trans'
- Resolves: rhbz#1331338

- update to 1.4.2
- Fix mistyped variable name
- Resolves: rhbz#1330461
- Add option to remember the preëdit input method used last
- Update German translations
- The combobox in the setup tool should show the first supported ime
  from dconf

* Wed Apr 20 2016 Mike FABIAN <mfabian@redhat.com> - 1.4.1-1
- update to 1.4.1
- Avoid unnessary initialization of transliterators when the set
  of input methods has not changed
- Add  property menu to choose the current preedit input method
- Display preëdit input method in aux_string also when number of
  candidates is not shown
- Add some tooltips to the setup tool
- Update German translations

* Sat Apr 09 2016 Mike FABIAN <mfabian@redhat.com> - 1.4.0-3
- update to 1.4.0
- Call IBus.Bus() in __main__, not in __init__ of class SetupUI
- Resolves: rhbz#1325338
- Multilingual support, more than one language in an engine
- Simple option in the setup tool to enable bilingual support
  (i.e. one language + Enlish).
- The default of the option “Add direct input” in the setup tool
  should be false (bug found by Pravin Satpute).
- Changing the main input method with the setup tool should not
  remove the direct input (bug found by Pravin Satpute)
- Add 0 as a digit to commit directly when using digits as select keys
- Clear dictionaries in Hunspell class before reloading

* Mon Feb 08 2016 Mike FABIAN <mfabian@redhat.com> - 1.3.1-1
- update to 1.3.1
- Use new transliterator  from m17n_translit.py also when switching
  input methods in the setup tool
- Resolves: rhbz#1304677

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Mike FABIAN <mfabian@redhat.com> - 1.3.0-3
- update to 1.3.0
- Use libm17n directly instead of going through libtranslit
- Forward key events triggering a commit using "forward_key_event()"
  instead of relying on "return False"
- Resolves: rhbz#1291238
- Add code to use F1-F9 as well as keys to select candidates
  for commit or remove
- Don not commit invisible candidates with select keys with numbers
  greater than the length of a page of the candidate list
- Control-arrow-left and Control-arrow-right now commit when
  the edges of the preedit string are reached
- Alt-<number> does not delete a prediction anymore,
  now only Control-<number> does this
- Add an option to disable the use of the digits 1-9 as
  selection keys (useful if one wants easier number input,
  selection then works only with the F1-F9 keys)
- Support input methods using AltGr (e.g. mr-inscript2)
  and Alt keys (e.g. ta-lk-renganathan)
- Resolves: rhbz#1051405
- Resolves: rhbz#772665

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Mike FABIAN <mfabian@redhat.com> - 1.2.15-1
- Use open() instead of codecs.open() to make the input method help button work again
- Resolves: rhbz#1276992

* Tue Sep 22 2015 Mike FABIAN <mfabian@redhat.com> - 1.2.14-2
- Fix wrong bug number in changelog
- Resolves: rhbz#1268153

* Tue Sep 22 2015 Mike FABIAN <mfabian@redhat.com> - 1.2.14-1
- Add Catalan translations, thanks to Robert Antoni Buj Gelonch <rbuj@fedoraproject.org>
- Resolves: rhbz#1268153
- Add Catalan engine
- Update German translations
- Add optional debug code
- Fix some pylint warnings

* Tue Sep 22 2015 Mike FABIAN <mfabian@redhat.com> - 1.2.13-1
- Add a property to start the setup tool
- Resolves: rhbz#1260088

* Thu Aug 27 2015 Mike FABIAN <mfabian@redhat.com> - 1.2.12-1
- Use open() instead of codecs.open() to fix dictionary loading problem on F23
- Resolves: rhbz#1257465

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.2.11-2
- Register as an AppStream component.

* Wed Sep 24 2014 Mike FABIAN <mfabian@redhat.com> - 1.2.11-1
- Require Python >= 3.3
- Always write xml output in UTF-8 encoding, not in the encoding of the current locale
- Change class “KeyEvent” to store the keycode as well
- Commit when hitting the borders of the preëdit with the arrow keys (Resolves: rhbz#1140502)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 17 2014 Mike FABIAN <mfabian@redhat.com> - 1.2.10-2
- Resolves: rhbz#1075892 update package URL to typingbooster.org

* Thu Feb 27 2014 Mike FABIAN <mfabian@redhat.com> - 1.2.10-1
- make profiling work again and make it easier to use
- port from Python2 to Python3
- add python-enchant support

* Fri Jan 17 2014 Mike FABIAN <mfabian@redhat.com> - 1.2.9-1
- Fix behaviour of arrow right keys in preëdit (Resolves: rhbz#1049324)
- Add timestamps to entries in the user database
- Add timestamp support to user_transliteration.py
- Use a single user database for all engines
- Add *-inscript2 transliteration options to the Indian languages where these were still missing (Resolves: rhbz#1051405)
- Make it possible to use multiple hunspell dictionaries at the same time
- Make it possible to specify a list of dictionaries in the config files
- Make it possible to get a word back into preëdit by using backspace (Resolves: rhbz#1032442)

* Fri Dec 20 2013 Anish Patil <apatil@redhat.com> - 1.2.8-1
- Change of IME name for oriya language  Resolves: rhbz#1045299
- Fixed issue multiple instances of setup menu Resolves: rhbz#1045294

* Wed Nov 20 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.7-1
- Don’t strip characters with Unicode category “Cf” (Other, format) from tokens (Resolves: rhbz#1032504)

* Thu Nov 14 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.6-1
- Change wording of the option to show the total number of candidates (Resolves: rhbz#1029748)
- Commit candidate clicked on with the mouse (Resolves: rhbz#1029822)
- Use direct input also for IBus.InputPurpose.PIN
- remove unused und superfluous arguments of constructor of Hunspell class
- Add some transliteration options to .conf files which had only native keyboard enabled

* Fri Oct 11 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.5-1
- Add feature to display input method description to setup tool (Resolves: rhbz#1001581)
- Remove the options “m17n_mim_name” and “other_ime” from the .conf files
- remove tab_enable option from config files

* Tue Oct 01 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.4-3
- Resolves: rhbz#1013992 ibus-typing-booster needs to have ibus write-cache --system in %%post and %%postun

* Mon Sep 30 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.4-2
- remove superfluous line break in changelog

* Sat Sep 28 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.4-1
- Use normalization form NFD internally for Korean as well
- Add check for input purpose for gnome-shell password dialog (Resolves: rhbz#1013008 - ibus-typing-booster shows entered text in password fields)

* Mon Sep 16 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.3-3
- remove obsoletes/provides, not needed anymore for Fedora >= 21

* Tue Aug 06 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.3-1
- Update to 1.2.3 upstream version
- Fix exception handling when trying to install a rpm package (Resolves: rhbz#986178)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.2-1
- Update to 1.2.2 upstream version
- Commit immediately when certain punctuation characters are typed and transliteration is not used (Resolves: rhbz#981179)
- Add an option to try completion only when a minimum number of characters has been typed

* Wed Jul 03 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.1-1
- Update to 1.2.1 upstream version
- Pop up a message box when a file has been read to train the database, indicating success or failure (Resolves: rhbz#979933)
- Update German translation
- Ignore most punctuation characters and mathematical symbols when tokenizing (Resolves: rhbz#979939)

* Fri Jun 28 2013 Mike FABIAN <mfabian@redhat.com> - 1.2.0-1
- Update to 1.2.0 upstream version
- Make TAB when used to enable/disable the lookup table work as a toogle
- Create a VIEW for “LIKE input_phrase%” in select_words() and use that
  in the following SELECT statements (Makes candidate calculation more
  than 10 times faster)

* Mon Jun 24 2013 Mike FABIAN <mfabian@redhat.com> - 1.1.0-1
- Update to 1.1.0 upstream version
- Add a commit=True parameter to check_phrase_and_update_frequency()
- Fix that the page_size is shown as 0 in the setup tool if it has not been set before
- Do not use AUTOINCREMENT
- Make it possible to exit the setup tool by typing Control-C in the terminal
- Add feature to read a text file for training the user database
- Update German translations and .pot file
- Fix error when the hunspell dictionary for an engine is missing

* Tue Jun 18 2013 Mike FABIAN <mfabian@redhat.com> - 1.0.3-1
- Update to 1.0.3 upstream version
- Don’t output page_size in “/usr/libexec/ibus-engine-typing-booster --xml” (Resolves: rhbz#975449 - ibus-daemon prints warnings because “/usr/libexec/ibus-engine-typing-booster --xml” prints the invalid element “page_size”)
- Use ~/.local/share/ibus-typing-booster/ to store user data and log files (Resolves: rhbz#949035 - don't use a hidden directory under .local/share)

* Fri Jun 14 2013 Mike FABIAN <mfabian@redhat.com> - 1.0.2-1
- Update to 1.0.2 upstream version
- Push context *after* writing the trigram to the database

* Fri Jun 14 2013 Mike FABIAN <mfabian@redhat.com> - 1.0.1-1
- Update to 1.0.1 upstream version
- Fix problem when IBUS_TYPING_BOOSTER_DEBUG_LEVEL is not set

* Thu Jun 13 2013 Mike FABIAN <mfabian@redhat.com> - 1.0.0-1
- Update to 1.0.0 upstream version
- Remove mudb and use “Write-Ahead Logging”
- Introduce an environment variable IBUS_TYPING_BOOSTER_DEBUG_LEVEL for debugging
- Speed up converting an old database to the current format
- Make prediction more intelligent by using context of up to 2 previous words
- Automatically remove whitespace between the last word and a punctuation character ending a sentence

* Sun Jun 02 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.32-1
- Update to 0.0.32 upstream version
- Resolves: rhbz#969847 - Editing in the preëdit of ibus-typing-booster behaves weird, especially with transliteration
- Fix behaviour of Control+Number
- When committing by typing TAB, update frequency data in user database
- When committing by tying RETURN or ENTER, update frequency data in user database
- Do not try to match very long words in the hunspell dictionaries
- Rewrite the code for moving and editing within the preëdit (rhbz#969847)
- Fix encoding error when changing values with the setup tool
- Add ko_KR.conf and ko_KR.svg
- Use normalization forms NFD or NFKD internally and NFC externally
- Remove old way of using libtranslit via ctypes
- Get rid of “freq” column in databases
- Remove too simpleminded auto-capitalization

* Wed May 29 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.31-1
- Update to 0.0.31 upstream version
- Resolves: rhbz#968209 - Typing characters which are not explicitly listed as “valid_input_chars” in .conf files in ibus-typing-booster get inserted in a weird position
- Remove lots of unused and/or useless code
- Simplify some code
- Fix the problem that after “page down” the first “arrow down” does not move down in the lookup table
- Never use “-” or “=” as page up and page down keys
- Print more useful debug output when an exception happens
- Replace unencodable characters when asking pyhunspell for suggestions
- Get dictionary encoding from .aff file
- Get rid of the the variable “valid_input_chars” (rhbz#968209)
- Remove option “valid_input_chars” from .conf files and template.txt
- Replace keysym2unichr(key.code) with IBus.keyval_to_unicode(key.code)

* Sun May 26 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.30-1
- Update to 0.0.30 upstream version
- simplify database structure and code
- The Swedish hunspell dictionary is in UTF-8, not ISO-8859-1
- SQL LIKE should behave case sensitively
- Do not throw away the input phrase in hunspell_suggest.suggest()
- Merge candidates which have the same resulting phrase in select_words()
- Remove phrases always from the user database when typing Alt+Number
- Sync memory user database “mudb” to disk user database “user_db” on focus out
- Delete all records from mudb after syncing to user_db
- Do not prevent phrases of length < 4 to be added to the frequency database
- Resolves: #966947 - When typing a/ with the da_DK ibus-typing-booster, one gets weird matches like a/ACJSTVW
- Do not use lang_chars for matching in the hunspell dictionaries, return immediately if input contains a “/” (Resolves: #966947)
- Remove lang_chars variable
- Use re.escape() to escape the string typed by the user correctly for use in a regular expression
- When removing a phrase with Alt+Number, remove it independent of the input_phrase

* Tue May 14 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.29-1
- Update to 0.0.29 upstream version
- Resolves: #962609  - [abrt] ibus-typing-booster-0.0.28-1.fc19: main.py:107:__init__:AttributeError: tabsqlitedb instance has no attribute 'get_ime_property' (Fix setup tool to use the new class for parsing the config files)
- Avoid adding duplicates to the database by checking first whether phrase is already there in add_phrase()

* Fri May 10 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.28-1
- Update to 0.0.28 upstream version
- Resolves: #961923 - python /usr/share/ibus-typing-booster/engine/main.py --xml is extremely slow when many hunspell dictionaries are installed
- Put the input phrase into a single column in the databases instead of using one column for each character
- Get rid of tab_dict

* Mon May 06 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.27-1
- Update to 0.0.27 upstream version
- Resolves: #959860 - [as_IN] Wrong keymap name Assami (fix spelling error in language name for Assamese)
- Resolves: #958770 - [ibus-typing-Booster][gu-IN]- Typo error (fix spelling error in language name for Gujarati)
- Resolves: #875285 - IME names too long in gnome-shell Input Sources indicator (remove ✓ from symbol in the .conf files)
- simplify code in select_words()
- remove some unused functions

* Thu Feb 14 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.26-1
- Update to 0.0.26 upstream version
- Resolves: #910986 - The arrow icons at the bottom of the candidate lookup table of ibus-typing-booster do not work
- Use different .svg icons for all engines
- Increase number of suggestions from hunspell
- Use the auxiliary text to display the number of candidates
- Make the display of the number of candidates in the auxiliary text optional
- Display of the number of candidates needs to be updated on page-up and page-down

* Thu Feb 14 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.25-1
- Update to 0.0.25 upstream version
- Port to use pygobject3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.24-1
- Update to 0.0.24 upstream version
- Resolves: #884808 - ibus-typing-booster should also show candidates which correct spelling errors
- Use pyhunspell to add spell-checking suggestions
- Use underline for preedit
- Colourize spellchecking suggestions and system phrases already used

* Fri Nov 23 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.23-1
- Update to 0.0.23 upstream version
- Resolves: #879261  dictionary is not automatically reloaded when it is installed via the setup tool
- Make the engine reload the dictionary when the dictionary is installed via the setup tool

* Wed Nov 14 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.22-1
- Update to 0.0.22 upstream version
- Resolves: #876666 Properties of ibus-typing-booster to select input methods are not shown by gnome-shell in f18
- Make the engine use the input method from the dconf setting
- Add combobox to setup GUI to select input method
- Update German translation

* Mon Nov 12 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.21-1
- Update to 0.0.21 upstream version
- Resolves: #875285 Shorten symbol displayed in gnome panel
- Add space before ( in long display name

* Thu Nov 08 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.20-1
- Update to 0.0.20 upstream version
- Resolves: #874421
- Improve setup GUI to make correct dictionary installable (Resolves #874421)
- Add page size spin button to setup tool
- Connect signals in __init__ of SetupUI after setting the initial values
- Make the setup tool find the right config file in gnome-shell on Fedora 18
- Update German translation

* Tue Nov 06 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.19-1
- Update to 0.0.19 upstream version
- fix rpmlint warning “incorrect-fsf-address”

* Wed Oct 31 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.18-1
- Update to 0.0.18 upstream version
- Resolves: #871056
- Save setup option “Enable suggestions by Tab Key” correctly in dconf (Resolves: #871056)
- Make setup dialog translatable and add German translations

* Wed Oct 24 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.16-1
- Update to 0.0.16 upstream version
- Resolves: #869687
- Make enabling the lookup table with the TAB key work correctly
- Simplify code in add_input()
- Make German input typed in NFD work

* Mon Oct 22 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.15-1
- Update to 0.0.15 upstream version
- Resolves: #869050
- Make sure the lookup table is hidden if there are no candidates to suggest (#869050)

* Mon Oct 22 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.14-1
- Update to 0.0.14 upstream version
- Show an obvious warning when the hunspell dictionary needed is not found
- Show exact matches in the .dic files as suggestions as well
- Do not forget the input method used last when activating a previously used engine
- Make spelling of the value of “symbol” in the .conf files more consistent
- include the file ru_RU.conf

* Thu Oct 18 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.13-1
- Update to 0.0.13 upstream version, in 0.0.12 I forgot to
  include the file de_DE.conf

* Thu Oct 18 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.12-1
- Update to 0.0.12 upstream version, in 0.0.11 I forgot to
  include the file keysym2ucs.py

* Thu Oct 18 2012 Mike FABIAN <mfabian@redhat.com> - 0.0.11-1
- Upstream has released 0.0.11 version containing the following
  improvements:
- Add .conf files for many languages and improve some existing .conf files
- Read other_ime option case insensitively
- Split only at the first = in a line in a .conf file
- Fix the problem that the user defined phrases are lost when switching engines
- use “layout = default” instead of “layout = us” in all .conf files
- Make sure the input of transliterate() is UTF-8 encoded
- Add a keysym2unichr() function and use it to support languages which have non Latin1 input
- Let first letter start with index 1 in autogenerated tabdict
- Use autogenerated tabdict always, not only in m17n mode
- Use special value 'NoIme' to indicate that no input method should be used
- Use contents of lang_chars for the regexp to match words in the dictionaries
- In process_key_event, do not return False when a non-ASCII character has been typed
- Read option valid_input_chars as UTF-8
- Use the encoding option from the .conf file always, not only in m17n mode
- Whether m17n mode is used should depend on the .conf file, not the language
- Use correct encoding to decode the dictionary file
- Some other minor fixes

* Wed Sep 26 2012 Anish Patil <apatil@redhat.com> - 0.0.10-1
- Upstream has released new version.

* Thu Sep 13 2012 Anish Patil <apatil@redhat.com> - 0.0.9-1
- Upstream has released new version.

* Tue Aug 14 2012 Anish Patil <apatil@redhat.com> - 0.0.8-1
- Upstream has released new version.

* Tue Jul 17 2012 Anish Patil <apatil@redhat.com> - 0.0.7-1
- The first version.
- derieved from ibus-table developed by Yu Yuwei <acevery@gmail.com>
