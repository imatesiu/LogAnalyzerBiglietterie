package cnr.isti.sse.big.rest.impl;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.ws.rs.Consumes;
import javax.ws.rs.POST;
import javax.ws.rs.Path;
import javax.ws.rs.core.Context;
import javax.ws.rs.core.MediaType;
import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Unmarshaller;

import org.apache.commons.io.IOUtils;
import org.apache.commons.lang3.ArrayUtils;
import org.apache.commons.lang3.tuple.ImmutableTriple;
import org.glassfish.jersey.media.multipart.FormDataBodyPart;
import org.glassfish.jersey.media.multipart.FormDataContentDisposition;
import org.glassfish.jersey.media.multipart.FormDataMultiPart;
import org.glassfish.jersey.media.multipart.FormDataParam;

import com.google.common.primitives.Bytes;
import com.sun.jersey.core.util.ReaderWriter;

import cnr.isti.sse.big.data.transazioni.LogTransazione;
import cnr.isti.sse.big.util.Utility;
import io.swagger.v3.oas.annotations.OpenAPIDefinition;
import io.swagger.v3.oas.annotations.info.Info;
import io.swagger.v3.oas.annotations.media.Content;
import io.swagger.v3.oas.annotations.media.Schema;
import io.swagger.v3.oas.annotations.parameters.RequestBody;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.servers.Server;



@OpenAPIDefinition(info = @Info(title = "APID Service", version = "0.1"), servers = {@Server(url="/v1/dispositivi")
})
//@Consumes(MediaType.MULTIPART_FORM_DATA)
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
			mediaType = MediaType.MULTIPART_FORM_DATA,
			schema = @Schema(implementation = LogTransazione.class)
			),
	description = "." )
	public String putLogTransazione(byte[] ricevute, @Context HttpServletRequest request, @Context HttpServletResponse response)
			throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************LogTransazione********************");
		try{

			log.info("Message from: "+request.getRemoteAddr());

			boolean	result = Utility.verifyPKCS7(ricevute);
			log.info(result);

			byte[] t = 	Utility.getData(ricevute);
			String LogTransazione = new String(t);
			String LT = LogTransazione.replaceAll("<!DOCTYPE LogTransazione SYSTEM.*", "");
			JAXBContext jaxbContext = JAXBContext.newInstance(LogTransazione.class);
			Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
			Utility.validateXmlLogTransazione(unmarshaller);	

			StringReader reader = new StringReader(LT);
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

	@Path("/ListLogTransazioneListFile")
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
			mediaType = MediaType.MULTIPART_FORM_DATA//,
			//	schema = @Schema(implementation = List<byte[]>.class)
			),
	description = "." )
	@Consumes(MediaType.MULTIPART_FORM_DATA)
	public String putLogTransazioneFiles( @FormDataParam("files") List<FormDataBodyPart> uploadedInputStream,
			@FormDataParam("files") List<FormDataContentDisposition> fileDetail, @Context HttpServletRequest request, @Context HttpServletResponse response)
					throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************List***LogTransazione********************");
		try{

			log.info("Message from: "+request.getRemoteAddr());




			List<ImmutableTriple<Integer, Integer, Integer>> limm = new ArrayList<ImmutableTriple<Integer,Integer,Integer>>();


			for(FormDataBodyPart filePart: uploadedInputStream) {
				byte[] your_primitive_bytes = IOUtils.toByteArray(filePart.getEntityAs(InputStream.class));




				boolean	resul = Utility.verifyPKCS7(your_primitive_bytes);
				log.info(resul);

				byte[] t = 	Utility.getData(your_primitive_bytes);
				String LogTransazione = new String(t);
				String LT = LogTransazione.replaceAll("<!DOCTYPE LogTransazione SYSTEM.*", "");
				JAXBContext jaxbContext = JAXBContext.newInstance(LogTransazione.class);
				Unmarshaller unmarshaller = jaxbContext.createUnmarshaller();
				Utility.validateXmlLogTransazione(unmarshaller);	

				StringReader reader = new StringReader(LT);
				LogTransazione LogT = (LogTransazione) unmarshaller.unmarshal(reader);

				limm.add(Utility.check(LogT));
			}
			ImmutableTriple<Integer, Integer, Integer> sum = Utility.sumImmutableTriple(limm);
			log.info("Logs: "+sum);
			String text = "KO";
			return text;
			//throw new WebApplicationException(Response.status(406).entity(text).build());



		} catch (Exception e) {
			e.printStackTrace();
			log.error(e);
		}
		return "";

	}

	@Path("/ListLogTransazioneFile")
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
			mediaType = MediaType.MULTIPART_FORM_DATA//,
			//	schema = @Schema(implementation = List<byte[]>.class)
			),
	description = "." )
	@Consumes(MediaType.MULTIPART_FORM_DATA)
	public String putLogTransazionel( @FormDataParam("file") InputStream uploadedInputStream,
			@FormDataParam("file") FormDataContentDisposition fileDetail, @Context HttpServletRequest request, @Context HttpServletResponse response)
					throws JAXBException {// DatiCorrispettiviType Corrispettivi,
		// @Context HttpServletRequest request){
		response.setHeader("Connection", "Close");
		log.info("****************LogTransazione********************");
		try{

			log.info("Message from: "+request.getRemoteAddr());


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
