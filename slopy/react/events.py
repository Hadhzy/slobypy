from slopy.rpc import Event


class MouseEvent:
    def on_click(self, event: Event):
        """
        This method is called when the component is clicked.

        ### Arguments
        - event: The `event` object that was emitted by `slopy`

        ### Returns
        - None
        """
        pass


class KeyboardEvent:
    pass


class ClipboardEvent:
    pass


class FormEvent:
    pass


class FocusEvent:
    pass


class TouchEvent:
    pass


class UIEvent:
    pass


class WheelEvent:
    pass


class SelectionEvent:
    pass


class ImageEvent:
    pass


class AnimationEvent:
    pass


class TransitionEvent:
    pass