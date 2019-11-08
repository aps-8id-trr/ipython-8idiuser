logger.info(__file__)

"""local overrides of Devices, usually to fix something broken"""

from ophyd import Kind


def safeOphydName(text):
    """
    make text safe to be used as an ophyd object name

    Given some input text string, return a clean version.
    Remove troublesome characters, perhaps other cleanup as well.
    This is best done with regular expression pattern matching.
    """
    import re
    pattern = "[a-zA-Z0-9_]"

    def mapper(c):
        if re.match(pattern, c) is not None:
            return c
        return "_"

    return "".join([mapper(c) for c in text])


class FixScalerCH(ScalerCH):

    def select_channels(self, chan_names=[]):
        '''Select channels based on the EPICS name PV

        Parameters
        ----------
        chan_names : Iterable[str] or None

            The names (as reported by the channel.chname signal)
            of the channels to select.
            If *None*, select all channels named in the EPICS scaler.
        '''
        self.match_names()  # name channels by EPICS names
        name_map = {}
        for i, s in enumerate(self.channels.component_names):
            channel = getattr(self.channels, s)
            # just in case the name is not yet safe
            channel.s.name = safeOphydName(channel.s.name)
            nm = channel.s.name  # as defined in scaler.match_names()
            if i == 0 and len(nm) == 0:
                nm = "clock"        # ALWAYS get the clock channel
            if len(nm) > 0:
                name_map[nm] = s

        # previous argument was chan_names=None to select all
        # include logic here that allows backwards-compatibility
        if len(chan_names or []) == 0:    # default setting
            chan_names = name_map.keys()

        read_attrs = []
        for ch in chan_names:
            try:
                read_attrs.append(name_map[ch])
            except KeyError:
                raise RuntimeError("The channel {} is not configured "
                                    "on the scaler.  The named channels are "
                                    "{}".format(ch, tuple(name_map)))

        self.channels.kind = Kind.normal
        self.channels.read_attrs = list(read_attrs)
        self.channels.configuration_attrs = list(read_attrs)

        for i, s in enumerate(self.channels.component_names):
            channel = getattr(self.channels, s)
            if s in read_attrs:
                channel.s.kind = Kind.hinted
            else:
                channel.s.kind = Kind.normal