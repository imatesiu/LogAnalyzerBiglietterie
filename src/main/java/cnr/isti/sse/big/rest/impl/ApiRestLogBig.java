package cnr.isti.sse.big.rest.impl;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.math.BigDecimal;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Date;
import java.util.HashMap;
import java.util.Map;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.Consumes;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.QueryParam;
import javax.ws.rs.WebApplicationException;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.Response.Status;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;

import org.apache.commons.io.IOUtils;
import org.glassfish.grizzly.utils.Pair;

import cnr.isti.sse.big.data.transazioni.LogTransazione;
import cnr.isti.sse.big.util.Utility;
import io.swagger.v3.oas.annotations.Hidden;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.Parameter;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.parameters.RequestBody;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.servers.Server;



@OpenAPIDefinition(info = @Info(title = "APID Service", version = "0.1"), servers = {@Server(url="/v1/dispositivi")
})
@Consumes(MediaType.APPLICATION_XML)
// @Produces(MediaType.APPLICATION_XML)
@Path("/biglietterie")
public class ApiRestLogBig {
	
	private static org.apache.log4j.Logger log = org.apache.log4j.Logger.getLogger(ApiRestLogBig.class);

	@Path("/LogTransazione")
	@POST
	@ApiResponse(
	        responseCode = "200",
	        content = @Content(
	            mediaType = MediaType.APPLICATION_XML,
	            		schema = @Schema(implementation = String.class)
	        ),
	        description = "."
	    )
	@RequestBody(content = @Content(
			mediaType = MediaType.APPLICATION_XML,
			schema = @Schema(implementation = LogTransazione.class)
			),
	description = "." )
	public String putLogTransazione(String LogTransazione, @Context HttpServletRequest request, @Context HttpServletResponse response)
			throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************LogTransazione********************");
		try{
			
			log.info("Message from: "+request.getRemoteAddr());
			
			
			
			JAXBContext jaxbContext = JAXBContext.newInstance(LogTransazione.class);
			Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
			Utility.validateXmlLogTransazione(unmarshaller);	
			
			StringReader reader = new StringReader(LogTransazione);
			LogTransazione LogT = (LogTransazione) unmarshaller.unmarshal(reader);

			Utility.check(LogT);
			
			String text = "KO";
			return text;
			//throw new WebApplicationException(Response.status(406).entity(text).build());
		
		
		
		} catch (Exception e) {
			e.printStackTrace();
			log.error(e);
		}
		return "";
		
	}
	
	@Path("/LogSigillo")
	@POST
	@ApiResponse(
	        responseCode = "200",
	        content = @Content(
	            mediaType = MediaType.APPLICATION_XML,
	            		schema = @Schema(implementation = String.class)
	        ),
	        description = "."
	    )
	@RequestBody(content = @Content(
			mediaType = MediaType.APPLICATION_XML,
			schema = @Schema(implementation = LogTransazione.class)
			),
	description = "." )
	public String putLogSigillo(String LogSigillo, @Context HttpServletRequest request, @Context HttpServletResponse response)
			throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************LogSigillo********************");
		
		
		
		return "";
		
	}

}
