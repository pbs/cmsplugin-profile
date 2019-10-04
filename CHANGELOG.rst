CHANGELOG
=========

Revision 1373088 (04.10.2019, 15:43 UTC)
----------------------------------------

No new issues.

* Misc commits

  * Pin attrs package

Revision ce5a8ae (06.11.2018, 13:20 UTC)
----------------------------------------

No new issues.

* Misc commits

  * Pin pytest 3.4.0 and pytest-django 3.1.2

Revision 8228234 (06.05.2016, 15:25 UTC)
----------------------------------------

* LUN-2954

  * Change plugins to components.

No other commits.

Revision e66659d (08.04.2016, 07:18 UTC)
----------------------------------------

* LUN-2894

  * Use setuptools-tasks for compiling sass files before deploy.

No other commits.

Revision 4d53d70 (31.03.2016, 11:23 UTC)
----------------------------------------

* LUN-2951

  * profile promo fixes for 3 promos

No other commits.

Revision f7455db (23.03.2016, 10:00 UTC)
----------------------------------------

* LUN-2890

  * messages and help texts updated

* LUN-2947

  * add spinner when loading more profiles
  * css reviewed on load more profile items

* Misc commits

  * removed spinner also when error

Revision dc23d63 (16.03.2016, 09:58 UTC)
----------------------------------------

* LUN-2825

  * removed extra classes
  * misspelled variables after prettify
  * updates after code review
  * removed scollingToTop at deletion of an item
  * description texts updated, marked for deletion display updated
  * new status: marked for deletion item
  * tooltip updates
  * grids items with errors styled
  * profile promo message updated
  * css fixes for 4 promo items
  * fixed alignments between breakpoints + 4 on a row on Studio 2

* LUN-2890

  * Update profile grid delete warning message.
  * Use spaces instead of tabs.
  * Refactor validations.
  * Resize iframe after deleting an item.
  * Minor fixes.
  * Update rendering and validation for new/deleted profiles.
  * Do not remove deleted profiles from DOM, just mark them.
  * Remove dead code.
  * Draft for validation rework.
  * Show "unsaved" message when submit fails.
  * Update warnings.
  * Adjust warning messages.
  * Move formset errors to main error list.
  * Reset deleted flag when errors are shown.
  * Added validation that profile deletion does not break existing promos.
  * Enforce profile selection for Promo Grid on the backend.
  * Change validation to allow 3 or 4 profile selection in promo.

No other commits.

Revision c2183c9 (03.02.2016, 07:39 UTC)
----------------------------------------

* LUN-2829

  * Create the required many-to-one relations when plugins are copied.
  * Handle workflows that do not create the attribute unsaved_select_profiles.
  * Test for plugin copying.

* LUN-2869

  * firefox issue fixed on Studio 2

No other commits.

Revision e3cd839 (14.01.2016, 14:48 UTC)
----------------------------------------

* LUN-2813

  * new lines added manually werent calculated well

* LUN-2819

  * IE11 bug fixe
  * missing timestamp on grid

* LUN-2821

  * remove flex and added line-height to vertical aling images

* LUN-2823

  * profile promo updated
  * profile items alignments updated
  * pages with Profile Grid/Promo couldnt be saved - fixed
  * Profile fixed for station templates
  * Profile fixed on producer templates
  * Profile plugin fixed for Studio 2 cols
  * profile grid updates on Studio 2 cols

No other commits.

Revision 0293589 (25.11.2015, 11:00 UTC)
----------------------------------------

* LUN-2808

  * scrolling and resize on mobile/tablet fix

* LUN-2814

  * Also save the selection for the link target so it can be restored.
  * Fix values for profile link target selection.

* LUN-2816

  * added off() also on delegated function
  * multiple click triggers on link fixed with off()

* LUN-2817

  * Escape only html.

* LUN-2818

  * Fix: Input value with total form count was not increased correctly.

No other commits.

Revision 94d7f47 (23.11.2015, 10:31 UTC)
----------------------------------------

* LUN-2698

  * global variable transformed to local by mistake fixed
  * renamed js files that are dependent of jquery
  * missed comma  added
  * update after code review
  * namespaced the plugin so that we can have many grids/promos on a page
  * word-wraping added on other elements as well
  * convert tabs to spaces
  * Firefox bug fixed with max-width on image
  * prettify file
  * fix bug due to html entities
  * bug fixed with no-wrapping title

* LUN-2744

  * Fix bug: Profile selection was not maintained if validation failed.
  * New selected profiles were always added but never removed.
  * Move new_profile request in the admin url namespace.
  * Remove authentication check for front end "load more profiles" request.

* LUN-2807

  * Profile plugin issues fixed on dark theme

* LUN-2808

  * profile preview closes at window resize - fixed

* Misc commits

  * correct path to jquery resources for the grid

Revision 04a649e (17.11.2015, 13:36 UTC)
----------------------------------------

Changelog history starts here.
