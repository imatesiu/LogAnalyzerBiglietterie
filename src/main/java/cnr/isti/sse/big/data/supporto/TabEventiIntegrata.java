package cnr.isti.sse.big.data.supporto;

import javax.xml.bind.annotation.*;
import java.util.List;

@XmlAccessorType(XmlAccessType.FIELD)
@XmlType(name = "", propOrder = {
        "evento"
})
@XmlRootElement(name = "TabEventiIntegrata")
public class TabEventiIntegrata {

    @XmlElement(name = "Evento", required = true)
    protected List<TabEvento> evento;

    public List<TabEvento> getEvento() {
        return evento;
    }

    public void setEvento(List<TabEvento> evento) {
        this.evento = evento;
    }
}
