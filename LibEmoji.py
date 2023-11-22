"""
EasyTyping - a simplified notepad software
Copyright (C) 2023 Yiming Yang

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

face_smiling_emoji_list = ['😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', '🙃', '😉', '😊', '😇']
face_affection_emoji_list = ['🥰', '😍', '🤩', '😘', '😗', '😚', '😙']
face_tongue_emoji_list = ['😋', '😛', '😜', '🤪', '😝', '🤑']
face_hand_emoji_list = ['🤗', '🤭', '🤫', '🤔']
face_neutral_skeptical_emoji_list = ['🤐', '🤨', '😐', '😑', '😶', '😏', '😒', '🙄', '😬', '😮‍', '🤥', '🙂']
face_sleepy_emoji_list = ['😌', '😔', '😪', '🤤', '😴']
face_unwell_emoji_list = ['😷', '🤒', '🤕', '🤢', '🤮', '🤧', '🥵', '🥶', '🥴', '😵', '🤯']
face_concerned_emoji_list = ['😕', '😟', '🙁', '😮', '😯', '😲', '😳', '🥺', '😦', '😧',
                             '😨', '😰', '😥', '😢', '😭', '😱', '😖', '😣', '😞', '😓', '😩', '😫', '🥱']
face_negative_emoji_list = ['😤', '😡', '😠', '🤬', '😈', '👿', '💀']

emoji_dict = {
    'smiling': ['😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂', '🙂', '🙃', '😉', '😊', '😇'],
    'loving': ['🥰', '😍', '🤩', '😘', '😗', '😚', '😙'],
    'with tongue': ['😋', '😛', '😜', '🤪', '😝', '🤑'],
    'with hand': ['🤗', '🤭', '🤫', '🤔'],
    'neutral or skeptical': ['🤐', '🤨', '😐', '😑', '😶', '😏', '😒', '🙄', '😬', '😮‍', '🤥', '🙂'],
    'sleepy': ['😌', '😔', '😪', '🤤', '😴'],
    'unwell': ['😷', '🤒', '🤕', '🤢', '🤮', '🤧', '🥵', '🥶', '🥴', '😵', '🤯'],
    'concerned': ['😕', '😟', '🙁', '😮', '😯', '😲', '😳', '🥺', '😦', '😧',
                       '😨', '😰', '😥', '😢', '😭', '😱', '😖', '😣', '😞', '😓', '😩', '😫', '🥱'],
    'angry': ['😤', '😡', '😠', '🤬', '😈', '👿', '💀']
}


def is_valid_emoji(emoji: str):
    is_valid = False
    for emoji_list in emoji_dict:
        for ref_emoji in emoji_dict[emoji_list]:
            if ref_emoji.find(emoji) >= 0:
                is_valid = True
                break
    return is_valid


class Emoji:
    __my_emoji: str

    def __init__(self):
        self.__my_emoji = "😀"

    def get_emoji(self):
        return self.__my_emoji

    def set_emoji(self, emoji: str):
        emoji.replace(' ', '')
        if not is_valid_emoji(emoji):
            raise ValueError(f"{emoji} is not a registered emoji.")

        self.__my_emoji = emoji
