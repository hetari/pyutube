#### 1.5.22 (2026-05-05)

##### Chores

*  bump version (2b6ab898)

##### Documentation Changes

*  update installation instructions in README and add subtitle usage documentation (e0b5ddb7)
*  add DeepWiki badge to README (b0c79224)

##### New Features

*  add skip option to file conflict resolution and update single download service logic (7682523d)
*  add MP3 conversion support (7d8615c9)
*  add subtitle documentation, bump version, and include imageio-ffmpeg as a dependency (51b66845)

##### Refactors

*  replace raw subprocess calls with moviepy utilities and optimize audio conversion logic (407f1054)

#### 1.5.22 (2026-05-05)

##### Documentation Changes

*  update installation instructions in README and add subtitle usage documentation (e0b5ddb7)
*  add DeepWiki badge to README (b0c79224)

##### New Features

*  add skip option to file conflict resolution and update single download service logic (7682523d)
*  add MP3 conversion support (7d8615c9)
*  add subtitle documentation, bump version, and include imageio-ffmpeg as a dependency (51b66845)

##### Refactors

*  replace raw subprocess calls with moviepy utilities and optimize audio conversion logic (407f1054)

#### 1.5.2 (2026-05-03)

##### Chores

*  bump version to 1.5.2 and add documentation for subtitle handling (2121e823)
*  bump version to 1.5.1 and refactor package exports and setup configuration (192dbe1f)
*  standardize codebase, improve documentation, and refactor type annotations (bbf2d09b)
*  implement CI/CD pipeline, type checking, linting, and comprehensive test suite (69f26ea3)

##### New Features

*  add AudioConversionService to convert audio streams to MP3 and update download services accordingly (512de842)

##### Bug Fixes

*  prevent unnecessary version checks and downgrades, and rename stream loading spinner text (1346825e)

##### Refactors

*  update audio handling to use native containers, switch to subprocess for ffmpeg, adjust YouTube client configuration (31c37c7e)
*  use lazy imports for requests to handle missing dependency errors gracefully (78a8c2be)
*  modularize download services and implement dedicated file conflict resolution and video merging services (a7aeaaa2)
*  modularize URL parsing logic and introduce dedicated prompt and network services (23d9d30e)
*  improve playlist processing, add project documentation, and optimize download service logic (eb91d2a6)

##### Tests

*  implement comprehensive unit test suite for core services and handlers (2718fa61)

### 1.5.0 (2025-06-19)

##### Chores

*  update version to 1.5.0 (2939629c)

##### Bug Fixes

*  enhance video download check by cleaning filenames for better matching (d0ec7f11)
*  improve playlist video naming based on order preference (7f0150b3)

## 2.0.0 (2025-06-19)

##### Bug Fixes

*  enhance video download check by cleaning filenames for better matching (d0ec7f11)
*  improve playlist video naming based on order preference (7f0150b3)

#### 1.4.19 (2025-04-06)

##### Chores

*  replace LICENSE.md with LICENSE and update MANIFEST.in (fd4a005d)

##### Documentation Changes

*  update README.md for installation instructions and formatting improvements (52a44487)

##### Bug Fixes

*  update version to 1.4.19 and improve prompt message for playlist ordering (1f06e17e)
*  add --break-system-packages option to pip install for auto-update functionality (dd45d002)

#### 1.4.19 (2025-04-06)

##### Chores

*  replace LICENSE.md with LICENSE and update MANIFEST.in (fd4a005d)

##### Documentation Changes

*  update README.md for installation instructions and formatting improvements (52a44487)

##### Bug Fixes

*  add --break-system-packages option to pip install for auto-update functionality (dd45d002)

#### 1.4.18 (2025-02-15)

##### Chores

*  replace LICENSE.md with LICENSE and update MANIFEST.in (fd4a005d)

##### Documentation Changes

*  update README.md for installation instructions and formatting improvements (52a44487)

##### Bug Fixes

*  add --break-system-packages option to pip install for auto-update functionality (dd45d002)

#### 1.4.17 (2025-02-12)

##### Chores

*  update version to 1.4.17 and add to CHANGELOG (4d5737b8)

##### Bug Fixes

*  reverse playlist videos order before renaming titles (6ddd018d)
*  update uninstall command to break system packages (c8ebfcaf)

#### 1.4.17 (2025-02-12)

##### Bug Fixes

*  reverse playlist videos order before renaming titles (6ddd018d)
*  update uninstall command to break system packages (c8ebfcaf)

#### 1.4.16 (2025-01-22)

##### Bug Fixes

*  oAuth (29e62500)

#### 1.4.15 (2025-01-21)

#### 1.4.14 (2025-01-21)

##### Bug Fixes

*  auto updating library (507ffa76)

#### 1.4.14 (2025-01-21)

#### 1.4.13 (2024-12-31)

##### Bug Fixes

*  ensure nearest resolution is selected when desired resolution is unavailable (0e62f1a8)

#### 1.4.12 (2024-12-15)

##### Chores

*  update dependencies to their latest versions (6f164458)

##### Bug Fixes

*  download videos index error and converting error (7b9a09d9)
*  playlist video number (50a39410)
*  f-string error (6a065701)
*  keep video file without deleting it (184a718c)
*  delete video error (f2c537ae)
*  download file ext (9f7241c6)
*  video and audio file merging logic (69efb70d)

##### Other Changes

* upgrade the cli (4cb75ceb)
*  audio m4a file ext (75a1ae00)

#### 1.4.11 (2024-12-15)

##### Bug Fixes

*  playlist video number (50a39410)
*  f-string error (6a065701)
*  keep video file without deleting it (184a718c)
*  delete video error (f2c537ae)
*  download file ext (9f7241c6)
*  video and audio file merging logic (69efb70d)

##### Other Changes

* upgrade the cli (4cb75ceb)
*  audio m4a file ext (75a1ae00)

#### 1.4.10 (2024-12-15)

##### Bug Fixes

*  playlist video number (50a39410)
*  f-string error (6a065701)
*  keep video file without deleting it (184a718c)
*  delete video error (f2c537ae)
*  download file ext (9f7241c6)
*  video and audio file merging logic (69efb70d)

##### Other Changes

* upgrade the cli (4cb75ceb)
*  audio m4a file ext (75a1ae00)

#### 1.4.10 (2024-12-15)

##### Bug Fixes

*  playlist video number (50a39410)
*  f-string error (6a065701)
*  keep video file without deleting it (184a718c)
*  delete video error (f2c537ae)
*  download file ext (9f7241c6)
*  video and audio file merging logic (69efb70d)

##### Other Changes

* upgrade the cli (4cb75ceb)
*  audio m4a file ext (75a1ae00)

# Changelog

<!-- insertion marker -->

## Unreleased

<small>[Compare with latest](https://github.com/Hetari/pyutube/compare/1.3.29...HEAD)</small>

### Added

- add: automatically upgrade packages if a new version is available ([c31e4eb](https://github.com/Hetari/pyutube/commit/c31e4ebeb2ff57bdd7c45ef4f1804da4d6b709c2) by Hetari).

### Fixed

- fix: check_for_updates method ([2fecb30](https://github.com/Hetari/pyutube/commit/2fecb30b5400f36426566c383a165bbddaf983dd) by Hetari).

### Removed

- Remove all unit and integration tests from the codebase.

<!-- insertion marker -->

## [1.3.29](https://github.com/Hetari/pyutube/releases/tag/1.3.29) - 2024-10-06

<small>[Compare with 1.3.24](https://github.com/Hetari/pyutube/compare/1.3.24...1.3.29)</small>

### Fixed

- fix: cancel video download before selecting quality ([ae17d15](https://github.com/Hetari/pyutube/commit/ae17d15bb6c2cb53b31860985901a5e22af82480) by Hetari).
- fix utils ([a30a48e](https://github.com/Hetari/pyutube/commit/a30a48ea8961fde6beb597c9cd83d05d27eb98a9) by Hetari).

### Removed

- remove cache ([c5fc490](https://github.com/Hetari/pyutube/commit/c5fc4906d2b4a02836c46a0f429a3cd2b9934460) by Hetari).

## [1.3.24](https://github.com/Hetari/pyutube/releases/tag/1.3.24) - 2024-09-25

<small>[Compare with 1.3.21](https://github.com/Hetari/pyutube/compare/1.3.21...1.3.24)</small>

### Fixed

- fix VideoUnavailable error ([ffccfd3](https://github.com/Hetari/pyutube/commit/ffccfd3f1135527b85a86a55690da4d0b9561e01) by Hetari).
- fix f-string ([9958cdd](https://github.com/Hetari/pyutube/commit/9958cdd75f6f98175a384de4318864f5cad6ddf9) by Hetari).

## [1.3.21](https://github.com/Hetari/pyutube/releases/tag/1.3.21) - 2024-08-21

<small>[Compare with 1.2.9](https://github.com/Hetari/pyutube/compare/1.2.9...1.3.21)</small>

### Added

- ADD LOGGING ([623278d](https://github.com/Hetari/pyutube/commit/623278d13ebf932d8f3aa29a2a5b2d30f358a919) by Hetari).
- Add S from the SOLID principle ([9f8941b](https://github.com/Hetari/pyutube/commit/9f8941b9593887d797d63fcb98d6f383340b3b03) by Hetari).

### Fixed

- fix some issues ([3603b02](https://github.com/Hetari/pyutube/commit/3603b02102c6c139205b8fdb515af08297358625) by Hetari).
- fix rename name function ([3ce70a1](https://github.com/Hetari/pyutube/commit/3ce70a1c22a042b697d0345eca27f8ad9e33e043) by Hetari).
- fix check of update ([b9a662d](https://github.com/Hetari/pyutube/commit/b9a662d9eb41ceb7fb485a1a7109be32c7c75584) by Hetari).
- fix cli -a and -f options ([d85dffd](https://github.com/Hetari/pyutube/commit/d85dffdb2ff753a50fae17ba1161cb51825a9cd7) by Hetari).
- fix download audio ([5567c1a](https://github.com/Hetari/pyutube/commit/5567c1a41baf1e05c44b6d26f9f58a065e4b8274) by Hetari).
- fix the name func ([99b3e46](https://github.com/Hetari/pyutube/commit/99b3e46ebafa76481c95d634a807dad12c35c3bf) by Hetari).
- fix the playlist ([d5b1d7b](https://github.com/Hetari/pyutube/commit/d5b1d7b9e7a32d8c00c6ef52a46b9371e67f31b8) by Hetari).
- fix the video services ([e7b7f1a](https://github.com/Hetari/pyutube/commit/e7b7f1a63d38329a786f60f0a78633d933296b30) by Hetari).
- fix the audio services ([a46e445](https://github.com/Hetari/pyutube/commit/a46e445bf4cc081b5ddad3f548f9f619b60d2074) by Hetari).
- fix Unterminated string literal ([af3c0b7](https://github.com/Hetari/pyutube/commit/af3c0b74bbe1723d5273aefe3e6f793f71828d0f) by Hetari).
- fix naming files ([1330717](https://github.com/Hetari/pyutube/commit/13307178e0d80d676257250e5f951718c2b587f8) by Hetari).

### Removed

- remove unused variables ([0f2bdf8](https://github.com/Hetari/pyutube/commit/0f2bdf832f8d1e3966649cb83ae2a80b0ae40660) by Hetari).

## [1.2.9](https://github.com/Hetari/pyutube/releases/tag/1.2.9) - 2024-06-28

<small>[Compare with 1.2.8](https://github.com/Hetari/pyutube/compare/1.2.8...1.2.9)</small>

### Fixed

- fix: you can download live streams now ([eaa9792](https://github.com/Hetari/pyutube/commit/eaa97927184bfa1eb273813792efde9c6e493572) by Hetari).
- fix: improve cancel behavior in video quality selection ([1abf621](https://github.com/Hetari/pyutube/commit/1abf621fcaf4f0a3de4ea6f1e58f9dd2de841c1f) by Hetari).

## [1.2.8](https://github.com/Hetari/pyutube/releases/tag/1.2.8) - 2024-06-17

<small>[Compare with 1.2.4](https://github.com/Hetari/pyutube/compare/1.2.4...1.2.8)</small>

### Fixed

- fix: playlist download methods. ([32030d6](https://github.com/Hetari/pyutube/commit/32030d6b72ec6cf0f34e5d035edc6edcdba12ee7) by Hetari).
- fix dependencies ([4b9d45b](https://github.com/Hetari/pyutube/commit/4b9d45b08f99002ea8862e4f007026bf83cde547) by Ebraheem Alhetari).
- fix: switch into pytubefix instead of pytube ([cc88abc](https://github.com/Hetari/pyutube/commit/cc88abc083c0e86d4d62d01bc98510c84824f947) by Ebraheem Alhetari).
- Fix: Downloading error, (typo mistake) ([b7f10c4](https://github.com/Hetari/pyutube/commit/b7f10c486ed1b4c95b1517a1bff00af632864bab) by Ebraheem Alhetari).

## [1.2.4](https://github.com/Hetari/pyutube/releases/tag/1.2.4) - 2024-04-25

<small>[Compare with 1.2.1](https://github.com/Hetari/pyutube/compare/1.2.1...1.2.4)</small>

### Fixed

- fix: size calculation ([9d814a4](https://github.com/Hetari/pyutube/commit/9d814a4ff7d46d78aeab35224c37dbb748c9bc48) by Ebraheem Alhetari).

### Removed

- remove the cache ([7e75e02](https://github.com/Hetari/pyutube/commit/7e75e0289fc54e8147e1cd70fd0e70b38ad616ac) by Ebraheem Alhetari).

## [1.2.1](https://github.com/Hetari/pyutube/releases/tag/1.2.1) - 2024-04-20

<small>[Compare with 1.2.0](https://github.com/Hetari/pyutube/compare/1.2.0...1.2.1)</small>

### Added

- add images ([b60a1f8](https://github.com/Hetari/pyutube/commit/b60a1f875a6d05fdb1f9cea27410b42b7fc79c8f) by Ebraheem Alhetari).
- Add img ([31e49f9](https://github.com/Hetari/pyutube/commit/31e49f9b7ee436f6c1564114121f2415d1fb84fe) by Ebraheem Alhetari).

## [1.2.0](https://github.com/Hetari/pyutube/releases/tag/1.2.0) - 2024-04-11

<small>[Compare with 1.1.8](https://github.com/Hetari/pyutube/compare/1.1.8...1.2.0)</small>

### Added

- add version number ([aac923e](https://github.com/Hetari/pyutube/commit/aac923ea829e4cb99b9ec8874c99939d6850c313) by Ebraheem Alhetari).

### Fixed

- fix the setup.py to find packages ([5fcd4f2](https://github.com/Hetari/pyutube/commit/5fcd4f2f3daa5f5c76c545d7b4a3bcdc1b6835d1) by Ebraheem Alhetari).
- fix merge video and audio together ([0ba2f30](https://github.com/Hetari/pyutube/commit/0ba2f30ab4223ac15025d45aa6e0ca9e5ff8eee9) by Ebraheem Alhetari).

## [1.1.8](https://github.com/Hetari/pyutube/releases/tag/1.1.8) - 2024-04-02

<small>[Compare with 1.1.7](https://github.com/Hetari/pyutube/compare/1.1.7...1.1.8)</small>

### Added

- Add playlist supports ([759345a](https://github.com/Hetari/pyutube/commit/759345a823681c627aab2ada6533ca51721258fd) by Ebraheem Alhetari).

### Fixed

- fix the code with pylint ([fa3d22f](https://github.com/Hetari/pyutube/commit/fa3d22fe5bb6fab32694e7aa175bbb56865f5b08) by Ebraheem Alhetari).
- Fix bugs ([8679ce8](https://github.com/Hetari/pyutube/commit/8679ce89b8ae329809015c86ba96357fb4fdf736) by Ebraheem Alhetari).

## [1.1.7](https://github.com/Hetari/pyutube/releases/tag/1.1.7) - 2024-03-28

<small>[Compare with 1.1.5](https://github.com/Hetari/pyutube/compare/1.1.5...1.1.7)</small>

### Added

- add action ([2640f7c](https://github.com/Hetari/pyutube/commit/2640f7c40f4081b8a4e7a19c9f605d8e71bae0ea) by Ebraheem Alhetari).
- Add -a and -f options ([9abf118](https://github.com/Hetari/pyutube/commit/9abf118c19bf41dadc60bb22b2e3569f5a81c867) by Ebraheem Alhetari).
- Add the -v support ([71aeee8](https://github.com/Hetari/pyutube/commit/71aeee8cb6134160578dc8d9e25928ba99b6682d) by Ebraheem Alhetari).

## [1.1.5](https://github.com/Hetari/pyutube/releases/tag/1.1.5) - 2024-03-21

<small>[Compare with 1.1.4](https://github.com/Hetari/pyutube/compare/1.1.4...1.1.5)</small>

## [1.1.4](https://github.com/Hetari/pyutube/releases/tag/1.1.4) - 2024-03-20

<small>[Compare with 1.1.2](https://github.com/Hetari/pyutube/compare/1.1.2...1.1.4)</small>

### Fixed

- fix issues #1 ([3b62f48](https://github.com/Hetari/pyutube/commit/3b62f48f106ae7666f5425c32f28cbe75edcec19) by Ebraheem Alhetari).

## [1.1.2](https://github.com/Hetari/pyutube/releases/tag/1.1.2) - 2024-03-15

<small>[Compare with 1.1.0](https://github.com/Hetari/pyutube/compare/1.1.0...1.1.2)</small>

### Added

- Add feature: only available resolutions are listed ([cdd7aa3](https://github.com/Hetari/pyutube/commit/cdd7aa3bbb7d5e13bd22af147faf321fcb68b28d) by Ebraheem Alhetari).

### Fixed

- Fixes bugs ([678a34a](https://github.com/Hetari/pyutube/commit/678a34a8eefd8759c63901484ef965aafb10e782) by Ebraheem Alhetari).

## [1.1.0](https://github.com/Hetari/pyutube/releases/tag/1.1.0) - 2024-03-12

<small>[Compare with 1.0.1](https://github.com/Hetari/pyutube/compare/1.0.1...1.1.0)</small>

### Added

- Add shorts download ([17cf4d0](https://github.com/Hetari/pyutube/commit/17cf4d04132841568e3551bada613ddd6967789e) by Ebraheem Alhetari).

## [1.0.1](https://github.com/Hetari/pyutube/releases/tag/1.0.1) - 2024-03-09

<small>[Compare with first commit](https://github.com/Hetari/pyutube/compare/a390568062d001183f862a798a921a21d61015a6...1.0.1)</small>

### Added

- Add release notes ([e926a7f](https://github.com/Hetari/pyutube/commit/e926a7f9c0a00a4b9c44ce8a80d1863b4d7b396c) by Ebraheem Alhetari).
- Add more TODO ([05e41ee](https://github.com/Hetari/pyutube/commit/05e41ee2ba0c5f464c1bbb9497040d903e9de547) by Ebraheem Alhetari).
- Add comments and docs string in the code ([30d7483](https://github.com/Hetari/pyutube/commit/30d74832b2c11a8c3d7b8f67fccb23de068643c9) by Hetari).
- Add some missing requirements ([8280715](https://github.com/Hetari/pyutube/commit/828071573e82a7a658220e27dfda34becc0b0d4d) by Hetari).
- Add file name functionality ([dbc9a06](https://github.com/Hetari/pyutube/commit/dbc9a063ea27b4625040c098c13295506019b3aa) by Hetari).
- Add video download functionality ([75e0d80](https://github.com/Hetari/pyutube/commit/75e0d806b7fc3c88e9456cb9d33950315cb60c4f) by Hetari).
- Add the download_vide start function ([bdd03a1](https://github.com/Hetari/pyutube/commit/bdd03a17977214a386674fb68cc17233a50e738b) by Hetari).
- Add checking to the internet ([6d019b2](https://github.com/Hetari/pyutube/commit/6d019b2ca25a101f4b35f610e7d95e2b163fd200) by Hetari).
- Add requirements ([e2f4054](https://github.com/Hetari/pyutube/commit/e2f4054116ab66647f328c7e6669ef31a0311cb1) by Hetari).

### Fixed

- Fix: big fixing and update the endpoints ([9a5bc4a](https://github.com/Hetari/pyutube/commit/9a5bc4a48004a5090b3610bf0f4b0c4ca35ed50d) by Ebraheem Alhetari).
- Fix the Cli app and publish in PyPi ([954017f](https://github.com/Hetari/pyutube/commit/954017f5812151a0764a9202f0c3fd1bad7d6b2d) by Hetari).
- Fixing the error log ([1ed2327](https://github.com/Hetari/pyutube/commit/1ed2327f0f30333e07ccad4d96efcf8a00726a3c) by Hetari).
- Fixing the setup function so we can use the tool in every where ([85423f6](https://github.com/Hetari/pyutube/commit/85423f60fca85904829723631c6cb8e2136155ad) by Hetari).
- Fixing bug ([6b611ef](https://github.com/Hetari/pyutube/commit/6b611ef983ecfcd9cb28e96c763a1c1094179c68) by Hetari).
- Fixing the setup command ([63fe1a7](https://github.com/Hetari/pyutube/commit/63fe1a7216aa452d9d705430f104d61983f3e9f3) by Hetari).

### Removed

- remove python-publish.yml ([6663dbc](https://github.com/Hetari/pyutube/commit/6663dbcb0a21bb705c68c9591972382c22481c3a) by Hetari).
- remove if **name** == '**main**' ([57d3b74](https://github.com/Hetari/pyutube/commit/57d3b74051e1f7d972a16b64cb9b2e6976cd8e51) by Hetari).
